from datetime import datetime
from src.sentiment_analyzer.utils.logger import logger
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.sentiment_analyzer.news.fetch_financial_news import fetch_financial_news
from src.sentiment_analyzer.news.fetch_top_tickers import fetch_top_tickers
from src.sentiment_analyzer.sentiment.analyze_sentiment import analyze_sentiment
from src.sentiment_analyzer.database.store_sentiment_result import store_sentiment_result
from src.sentiment_analyzer.email.send_email_digest import send_email_digest
from src.sentiment_analyzer.utils.config import PERSONAL_TICKERS


default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 6, 25),
    "retries": 1,
}

def run_fetch(**context) -> list:
    """Fetch articles for all tickers (personal + top 10 active) and push to XCom."""
    top_tickers = fetch_top_tickers()
    all_tickers = list(set(PERSONAL_TICKERS + top_tickers))
    all_articles = []
    for ticker in all_tickers:
        articles = fetch_financial_news(ticker=ticker)
        for article in articles:
            article["ticker"] = ticker
        all_articles.extend(articles)
    logger.info(f"Fetched {len(all_articles)} total articles across {len(all_tickers)} tickers")
    return all_articles


def run_analyze(**context) -> list:
    """Pull articles from XCom, analyze each one, return list of sentiment results."""
    ti = context["ti"]
    articles = ti.xcom_pull(task_ids="fetch_financial_news")
    results = []
    for article in articles:
        results.append(analyze_sentiment(article=article))
    return results


def run_store(**context) -> list:
    """Pull sentiment results from XCom, store each one, return stored results."""
    ti = context["ti"]
    analysis = ti.xcom_pull(task_ids="analyze_sentiment")
    stored_results = []
    for result in analysis:
        stored_results.append(store_sentiment_result(ticker=result.get("ticker", "UNKNOWN"), sentiment_result=result))
    return stored_results


def run_email(**context) -> bool:
    """Pull stored results from XCom and send email digest."""
    ti = context["ti"]
    results = ti.xcom_pull(task_ids="store_sentiment_result")
    return send_email_digest(results=results, recipient="abhipatel867@gmail.com")


with DAG(
    dag_id="sentiment_pipeline",
    default_args=default_args,
    schedule_interval="0 7 * * *",
    catchup=False,
) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_financial_news",
        python_callable=run_fetch,
    )

    analyze_task = PythonOperator(
        task_id="analyze_sentiment",
        python_callable=run_analyze,
    )

    store_task = PythonOperator(
        task_id="store_sentiment_result",
        python_callable=run_store,
    )

    email_task = PythonOperator(
        task_id="send_email_digest",
        python_callable=run_email,
    )

    fetch_task >> analyze_task >> store_task >> email_task
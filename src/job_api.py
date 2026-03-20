import os
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Initialize Apify client
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not APIFY_API_TOKEN:
    raise ValueError("Missing APIFY_API_TOKEN in environment variables.")
apify_client = ApifyClient(APIFY_API_TOKEN)


def _fetch_jobs(actor_id: str, run_input: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Helper function to run an Apify actor and fetch dataset items.
    
    Args:
        actor_id (str): The Apify actor ID.
        run_input (dict): Input parameters for the actor.
    
    Returns:
        List[Dict[str, Any]]: List of job postings.
    """
    try:
        logging.info(f"Running actor {actor_id} with input: {run_input}")
        run = apify_client.actor(actor_id).call(run_input=run_input)
        dataset_id = run.get("defaultDatasetId")
        if not dataset_id:
            logging.error("No dataset ID returned from actor run.")
            return []
        jobs = list(apify_client.dataset(dataset_id).iterate_items())
        logging.info(f"Fetched {len(jobs)} jobs from actor {actor_id}.")
        return jobs
    except Exception as e:
        logging.error(f"Error fetching jobs from actor {actor_id}: {e}")
        return []


def fetch_linkedin_jobs(search_query: str, location: str = "india", rows: int = 60) -> List[Dict[str, Any]]:
    """
    Fetch LinkedIn jobs using Apify actor.
    
    Args:
        search_query (str): Job title or keyword.
        location (str): Job location.
        rows (int): Number of jobs to fetch.
    
    Returns:
        List[Dict[str, Any]]: List of LinkedIn job postings.
    """
    run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
    }
    return _fetch_jobs("BHzefUZlZRKWxkTck", run_input)


def fetch_naukri_jobs(search_query: str, location: str = "india", rows: int = 60) -> List[Dict[str, Any]]:
    """
    Fetch Naukri jobs using Apify actor.
    
    Args:
        search_query (str): Job keyword.
        location (str): Job location (not always used by Naukri actor).
        rows (int): Number of jobs to fetch.
    
    Returns:
        List[Dict[str, Any]]: List of Naukri job postings.
    """
    run_input = {
        "keyword": search_query,
        "maxJobs": rows,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
    }
    return _fetch_jobs("alpcnRV9YI9lYVPWk", run_input)

#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    
    ######################
    # YOUR CODE HERE     #
    ######################
    
    df = pd.read_csv(artifact_local_path, index_col="id")
    logger.info("Loaded data")
    
    indexes = df['price'].between(args.min_price, args.max_price)
    df = df[indexes].copy()
    
    logger.info("Dataset price outliers removal outside range:" + \
                f"{args.min_price}-{args.max_price}")

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    logger.info("Converted last_review to datetime")

    df.to_csv(args.output_artifact)

    # Upload artifact
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    
    artifact.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This steps cleans the data")

    parser.add_argument("--input_artifact", type=str)
    parser.add_argument("--output_artifact", type=str)
    parser.add_argument("--output_type", type=str)
    parser.add_argument("--output_description", type=str)
    parser.add_argument("--min_price", type=float, required=True)
    parser.add_argument("--max_price", type=float,)

    args = parser.parse_args()

    go(args)

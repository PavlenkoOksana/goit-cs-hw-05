import os
import shutil
import asyncio
import argparse
import logging

async def read_folder(source_path, target_path):
    for root, _, files in os.walk(source_path):
        for file in files:
            source_file_path = os.path.join(root, file)
            await copy_file(source_file_path, target_path)

async def copy_file(source_file_path, target_path):
    try:
        _, extension = os.path.splitext(source_file_path)
        extension = extension[1:]  # Видаляємо початкову крапку

        target_folder = os.path.join(target_path, extension)
        os.makedirs(target_folder, exist_ok=True)

        target_file_path = os.path.join(target_folder, os.path.basename(source_file_path))
        shutil.copy(source_file_path, target_file_path)

        logging.info(f"Successfully copied {source_file_path} to {target_file_path}")

    except Exception as e:
        logging.error(f"Error copying {source_file_path}: {str(e)}")

async def main():
    parser = argparse.ArgumentParser(description="Async file sorting script")
    parser.add_argument("source_folder", help="Source folder path")
    parser.add_argument("output_folder", help="Output folder path")
    args = parser.parse_args()

    source_path = os.path.abspath(args.source_folder)
    target_path = os.path.abspath(args.output_folder)

    if not os.path.exists(source_path):
        logging.error(f"Source folder '{source_path}' does not exist.")
        return

    logging.info(f"Sorting files from {source_path} to {target_path}...")

    await read_folder(source_path, target_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    asyncio.run(main())
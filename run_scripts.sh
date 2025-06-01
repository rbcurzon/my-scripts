echo "Starting the script execution..."

for i in {1..24}
do
    python3 ../my-scripts/scrape_chapter.py https://live.bible.is/bible/ILONGN/LUK/$i ILONGN
done

echo "Finished executing all scripts."
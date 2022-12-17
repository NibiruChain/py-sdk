poetry run pdoc nibiru -o=docs-md -f --skip-errors
mv docs-md/nibiru tmp
rm -rf docs-md
mv tmp docs-md

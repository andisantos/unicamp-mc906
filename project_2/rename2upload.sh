mkdir -p upload
for dir in $(ls outputs); do
    cp "outputs/"$dir"/plot.png" "upload/$dir.png"
done

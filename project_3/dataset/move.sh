root="./train_images/"
for t in $(ls $root); do
	i=0
	for p in $(ls $root$t); do
		for f in $(ls $root$t"/"$p); do
			i=$((i+1))
			mv $root$t"/"$p"/"$f $root$t"/"$i".png"
		done
		rmdir $root$t"/"$p
	done
done

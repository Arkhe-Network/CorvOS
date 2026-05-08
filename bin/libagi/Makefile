all:
	echo "void dummy(){}" > dummy.c && gcc -c dummy.c -o dummy.o && ar qc libagi.a dummy.o && rm dummy.c dummy.o

clean:
	rm -f libagi.a

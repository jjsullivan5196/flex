my @names = ('forward.csv', 'up.csv', 'right.csv', 'down.csv', 'left.csv');

opendir(my $dir, '.') or die $!;
my @files = readdir($dir);
splice(@files, 0, 2);
closedir($dir);

rename @files[$_], @names[$_] for (0 .. $#names);
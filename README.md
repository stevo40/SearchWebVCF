# SearchWebVCF
Binary Search of a 239GB VCF hosted on a web server.

Problem:
There are some vcf files which are inaccessible for analysis as they may be too big to download completely.

Sometimes we just need to extract one or two markers so do not need the entire file.

Solution:
The VCF is already ordered, so download snippets of the file using Binary Search, extract the position and find roughly where the marker is likely to be.

When we have a small enough space between partitions, we can download and parse the full block to return the required line of the vcf.  

Running:
```
seek(1, 22792776)

Subdivisions ordered:
0 212425 (1, 204)
1 14641250526 (1, 17511608)
2 18301535377 (1, 22292055)
3 18530316509 (1, 22561927)
4 18644693228 (1, 22693616)
5 18701895924 (1, 22754852)
6 18730490295 (1, 22786473)
7 18737676841 (1, 22790632)
8 18739489507 (1, 22792170)
9 18740384807 (1, 22792604)
10 18740507739 (1, 22792757) <----- search data was here
11 18740556540 (1, 22792779)
12 18740576312 (1, 22792794)
13 18740616217 (1, 22792799)
14 18740834221 (1, 22792921)
15 18741270023 (1, 22793112)
16 18744859518 (1, 22795741)
17 18759067255 (1, 22812318)
18 19216598992 (1, 23340406)
19 20131653330 (1, 24372497)
20 21961770103 (1, 26434631)
21 29282269363 (1, 36097201)
22 58564323697 (1, 74187951)
23 117128394949 (2, 25550613)
24 234256556816 (3, 86230358)
25 468512894916 (7, 39387489)
26 937025565836 (16, 4185967)
27 1874050917885 (88, 123869089)

result:chr1	22792776	.	A	G	231276.75	PASS	AC=761;AF=0.577;AN=1318;BaseQRankSum=-1.169e+00;ClippingRankSum=0.00;DP=10788;ExcessHet=-0.0000;FS=1.466;InbreedingCoeff=0.4031;MLEAC=781;MLEAF=0.593;MQ=43.36;MQRankSum=0.00;QD=30.99;ReadPosRankSum=0.00;SOR=0.887;VQSLOD=8.30;culprit=DP	GT:AD:DP:GQ:PGT:PID:PL:SAC	1/1:0,29:29:90:1|1:22792776_A_G:1235,90,0:0,0,12,17	0/0:22,0:22:60:.:.:0,60,900	....

```

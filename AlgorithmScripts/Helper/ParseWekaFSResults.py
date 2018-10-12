import sys

lines = []
hasReachedOutput = False
for line in sys.stdin:
    if hasReachedOutput:
        if line.strip() != "":
            lines.append(line.strip())

    if line.startswith("=== Attribute Selection on all input data"):
        hasReachedOutput = True

if "Ranked attributes:" in lines:
    lines = lines[(lines.index("Ranked attributes:") + 1):-1]

    print(",".join([line.split(" ")[-1] for line in lines]))
else:
    #### We can support this pretty easily. Just need to make sure output is comma delimited.
    print("Selected attributes not currently supported for Weka")
    sys.exit(1)
#    selectedAttributesStarted = False
#    for line in lines:
#        if selectedAttributesStarted:
#            if line.strip() != "":
#                print(line.strip())
#
#        if line.startswith("Selected attributes:"):
#            selectedAttributesStarted = True



#=== Attribute Selection on all input data ===
#
#Search Method:
#    Attribute ranking.
#
#Attribute Evaluator (supervised, Class (nominal): 101 Class):
#    Information Gain Ranking Filter
#
#Ranked attributes:
# 0.99819588     1 Feature1
# 0.99819588    24 Feature3
# 0.99819588    13 Feature2
# 0.99819588    46 Feature5
# 0.99819588    35 Feature4
# 0.36404613    50 Feature53
# 0.32440725    49 Feature52
# 0.32440725    51 Feature54
# 0.2871372     48 Feature51
# 0.21860436    52 Feature55
# 0.08864645    82 Feature82
# 0.06749386    53 Feature56
# 0.06510086    78 Feature79
# 0.05724553    65 Feature67
# 0.0481514     98 Feature97
# 0.0481514     83 Feature83
# 0.04568655    86 Feature86
# 0.04424727    58 Feature60
# 0.03534274    84 Feature84
# 0.0299614     73 Feature74
# 0.02845027    54 Feature57
# 0.02755253    95 Feature94
# 0.02187295    75 Feature76
# 0.01943138    94 Feature93
# 0.01633335    62 Feature64
# 0.0154003     88 Feature88
# 0.0154003     81 Feature81
# 0.0154003     64 Feature66
# 0.0154003     67 Feature69
# 0.01479486   100 Feature99
# 0.01450788    87 Feature87
# 0.01146205     3 Feature100
# 0.00857763    59 Feature61
# 0.00857763    93 Feature92
# 0.00857763    99 Feature98
# 0.00690069    69 Feature70
# 0.00690069    91 Feature90
# 0.00690069    77 Feature78
# 0.0063341     63 Feature65
# 0.00590682    76 Feature77
# 0.00590682    74 Feature75
# 0.00423525    70 Feature71
# 0.00336603    55 Feature58
# 0.00221165    85 Feature85
# 0.00180865    56 Feature59
# 0.00180865    92 Feature91
# 0.00180865    72 Feature73
# 0.00147926    60 Feature62
# 0.00147926    80 Feature80
# 0.00120498    61 Feature63
# 0.00097304    97 Feature96
# 0.00012056    66 Feature68
# 0.00004162    71 Feature72
# 0.00004162    89 Feature89
# 0.00000453    96 Feature95
# 0             45 Feature49
# 0             14 Feature20
# 0             57 Feature6
# 0             16 Feature22
# 0             15 Feature21
# 0             17 Feature23
# 0             22 Feature28
# 0             20 Feature26
# 0             19 Feature25
# 0             18 Feature24
# 0             12 Feature19
# 0             11 Feature18
# 0             10 Feature17
# 0             68 Feature7
# 0              2 Feature10
# 0              9 Feature16
# 0              4 Feature11
# 0              5 Feature12
# 0              6 Feature13
# 0              7 Feature14
# 0              8 Feature15
# 0             21 Feature27
# 0             23 Feature29
# 0             44 Feature48
# 0             37 Feature41
# 0             36 Feature40
# 0             39 Feature43
# 0             38 Feature42
# 0             40 Feature44
# 0             79 Feature8
# 0             43 Feature47
# 0             42 Feature46
# 0             41 Feature45
# 0             90 Feature9
# 0             34 Feature39
# 0             33 Feature38
# 0             26 Feature31
# 0             25 Feature30
# 0             32 Feature37
# 0             27 Feature32
# 0             28 Feature33
# 0             29 Feature34
# 0             30 Feature35
# 0             31 Feature36
# 0             47 Feature50
#
#Selected attributes:
#
#
#
#-----------------------------------------
#
#
#Selected attributes: 1,13,24,35,46,48,49,50,51,52,53,65 : 12
#                     Feature1
#                     Feature2
#                     Feature3
#                     Feature4
#                     Feature5
#                     Feature51
#                     Feature52
#                     Feature53
#                     Feature54
#                     Feature55
#                     Feature56
#                     Feature67

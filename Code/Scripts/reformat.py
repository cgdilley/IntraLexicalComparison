

langLines = []
with open('langs.txt', 'r') as langs:
    langLines = langs.readlines()

with open('kl.txt', 'r') as dist:
    with open('kl-final.txt', 'w') as kl_out:

        kl_out.write("52\n")
        for langLine in langLines:
            dataLine = dist.readline()

            vals = dataLine.split(' ')

            kl_out.write(langLine[:10] + "  ")
            for val in vals:
                if val is '\n':
                    continue
                kl_out.write(val + " ")
            kl_out.write("\n")


import requests
import sys
import yaml

re = requests.get("http://kancolle.wikia.com/wiki/" + sys.argv[1])

if re.status_code == 200:
    html = re.text
    try:
        quotes_raw = html.replace("\n", "").split('<tr><th>Time</th><th>Japanese</th><th>English</th><th>Note</th></tr><tr>')[1].split("<td></td></tr></table>")[0].replace("</td>", "")
        all_list = quotes_raw.split("<td>")
        hourlies = [all_list[x] for x in range(len(all_list)) if (x+1)%4==0]
        file = open("config/secretary.yml", "r")
        secr = yaml.load(file)
        file.close()
        new = sys.argv[1].replace("_", " ")
        secr[new] = hourlies
        print(sorted(secr.keys()))
        file = open("config/secretary.yml", "w")
        yaml.dump(secr, file, default_flow_style=False)
    except Exception as e:
        print("I couldn't find any hourly notifications.")
        print(e)
else:
    print("I didn't find", sys.argv[1], "and got", re.status_code)
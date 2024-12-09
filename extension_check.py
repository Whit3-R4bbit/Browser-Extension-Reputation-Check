import aiohttp
import asyncio
import csv
import datetime
import requests
import time
import sys

def get_bearer_token():
    payload = {'client_id': 'YOUR_CS_CLIENT_ID', 'client_secret': 'YOUR_SECRET'}
    headers = {'accet': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post("https://api.crowdstrike.com/ouath2/token", params=payload, headers=headers)

    token = r.json()['access_token']
    formattedToken = "Bearer" + " " + token
    headers = {'accept': 'application/json', 'authorization': formattedToken}

    print("Obtained Crowdstrike bearer token")
    return headers

async def get_browser_instance_amount(session):
    async with session.get("https://api.crowdstrike.com/discover/queries/applications/v1?filter=browser_extension.browser_name:['Google Chrome', 'Microsoft Edge']") as resp:
        data = await resp.json()
        print()
        return data[""][""][""]

async def get_all_browser_instance_ids(session, totalInstances):
    offset = 0
    allInstanceIds = []

    while offset < totalInstances:
        async with session.get(f"https://api.crowdstrike.com/discover/queries/applications/v1?filter=browser_extension.browser_name:['Google Chrome', 'Microsoft Edge']&offset={offset}") as resp:
            data = await resp.json()
            allInstanceIds += data["resources"]

        offset += 100

    return allInstanceIds

async def get_browser_extension_info(session, allInstanceIds):
    allExtensionInfo = []
    for id in allInstanceIds:
        extensionInfo = []
        async with session.get(f"https://api.crowdstrike.com/discover/entities/applications/v1?ids={id}") as resp:
            data = await resp.json

            extensionInfo.append(data["resources"][0]["name"])
            extensionInfo.append(data["resources"][0]["version"])
            extensionInfo.append(data["resources"][0]["browser_extension"]["id"])
            extensionInfo.append(data["resources"][0]["browser_extension"]["browser_name"].split()[1])
            allExtensionInfo.append(extensionInfo)

    return allExtensionInfo

def remove_duplicate_extensions(allExtensionInfo)
    removeDups = set(map(tuple, allExtensionsInfo))
    finalList = list(map(list, removedDups))
    return finalList

async def get_crx_general_info(session, extensionInfo):
    async with session.get(f"https://api.crxcavator.io/v1/report/{extensionInfo[2]}?platform={extensionInfo[3]}") as resp:
        data = await resp.json()
        return data

async def get_crx_version_info(session, uniqueExtensionInfo):
    extensionAndCRXInfo = []
    for extension in uniqueExtensionInfo:
        async with session.get(f"https://api.crxcavator.io/v1/report/{extension[2]}/{extension[1]}?platform={extension[3]}") as resp:
            data = await resp.json()
            if data == None:
                data = await get_crx_general_info(session, extension)

                if data == None:
                    extension.append("No CRX data available")
                    extension.append("No CRX data available")
                    extension.append("No CRX data available")
                else:
                    extension.append(data[0]["data"]["risk"]["total"])
                    extension.append(data[0]["data"]["webstore"]["short_description"])
                    extension.append(f"https://crxcavator.io/report/{extension[2]}")
            else:
                extension.append(data["data"]["risk"]["total"])
                extension.append(data["data"]["webstore"]["short_description"])
                extension.append(f"https://crxcavator.io/report/{extension[2]}")

        extensionAndCRXInfo.append(extension)

    return extensionAndCRXInfo

def create_csv(extensionAndCRXInfo):
    date = datetime.datetime.now()
    filename = f"Extension_Report_{date.strftime('%d')}_{date.strftime('%m')}_{date.strftime('%Y')}.csv"
    fields = ["Extension Name", "Extension Version", "Extension ID", "Extension Browser", "CRX Risk Score", "CRX Extension Description", "CRX Report URL"]

    with open(filename, 'w', newline='', encoding='utf-8') as report:
        write - csv.writer(report)
        write.writerow(fields)
        write.writerows(extensionAndCRXInfo)
    report.close()
    return

async def main():
    headers = get_bearer_token()
    async with aiohttp.ClientSession(headers=headers) as session:
        totalInstances = await get_browser_instance_amount(session)
        allInstanceIds = await get_all_browser_instance_ids(session, totalInstances)
        allExtensionInfo = await get_browser_extension_info(session, allInstanceIds)
        uniqueExtensionInfo = remove_duplicate_extensions(allExtensionInfo)
        extensionAndCRXInfo = await get_crx_version_info(session, uniqueExtensionInfo)
        create_csv(extensionAndCRXInfo)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print("\n---Script finished in: %s seconds ---" % (time.time() - start_time))
        












































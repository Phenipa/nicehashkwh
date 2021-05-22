import nicehash
import optparse


private_api = nicehash.private_api


debugs = False


def debug(text):
  if debugs == True:
    print(text)


def get_rigs():
  #### 
  # get_rigs returnerer en array av alle rig-id
  response = private_api.request('GET', '/main/api/v2/mining/groups/list', '', None)
  rigs = []
  for group in response['groups']:
    for rig in response['groups'][group]['rigs']:
      rigs.append(rig['rigId'])
  return rigs


def get_watts(rigs):
  ####
  # get_watts returnerer en liste over alle rigs som blir med som argument
  watts = 0
  dev_with_watt = []
  for rig in rigs:
    devices = private_api.request('GET', f'/main/api/v2/mining/rig2/{rig}', '', None)
  for d in devices["devices"]:
    if d["powerUsage"] != -1:
      watts += d["powerUsage"]
      dev_with_watt.append(d)
  average_watts = watts/len(dev_with_watt)
  if debugs:
    devices = []
    for d in dev_with_watt:
      devices.append(d['name'])
    debug(f'devices with watts: {devices}')
  debug(f'watts: {watts}')
  debug(f'average watts: {average_watts}')
  return average_watts


def get_time(rigs):
  timestamp = 000
  for rig in rigs:
    stats = private_api.request('GET', '/main/api/v2/mining/rig/stats/algo', f'rigId={rig}&algorithm=20&afterTimestamp={timestamp}', None)
  debug(len(stats['data']))
  debug(stats['data'][len(stats['data'])-1])
  return len(stats['data'])*5


def calc_kwh(minutes, rig_watts):
  # Calculate kWh
  result = rig_watts*minutes/60/1000
  return result


if __name__ == "__main__":
  # Get commandline options
  parser = optparse.OptionParser()
  parser.add_option('-d', '--debug', action='store_true', dest='debug', help='Show debug info', default=False)
  parser.add_option('-k', '--key', dest="key", help="Api key")
  parser.add_option('-s', '--secret', dest="secret", help="Secret for api key")
  parser.add_option('-o', '--organization_id', dest="org", help="Organization id")
  parser.add_option('-b', '--base_url', dest="base", help="Api base url", default="https://api2.nicehash.com")

  options, args = parser.parse_args()

  debugs = options.debug

  private_api = nicehash.private_api(options.base, options.org, options.key, options.secret)

  ####
  # kwh_current_wattage brukes fordi jeg per nå ikke kan hente annet enn ett datapunkt for mengden watt som brukes akkurat nå. Må evt. lagre watt-historikk selv.
  kwh_current_wattage = calc_kwh(get_time(get_rigs()), get_watts(get_rigs()))
  print(f'kWh: {kwh_current_wattage}')
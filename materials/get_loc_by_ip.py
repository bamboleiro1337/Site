import pygeoip
matc = pygeoip.GeoIP('GeoLiteCity.dat')
matc = matc.country_name_by_addr('176.125.33.252')
print(matc)
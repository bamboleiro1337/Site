import pygeoip
matc = pygeoip.GeoIP('GeoLiteCity.dat')
matc = matc.country_name_by_addr('10.240.5.141')

print(matc)
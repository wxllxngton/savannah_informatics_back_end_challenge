import http.client

conn = http.client.HTTPSConnection("savannah-informatics-back-end-challenge.onrender.com")

headers = { 'authorization': "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldUTjQwNG9UV1pjZ0U4dHpBVzBCcCJ9.eyJpc3MiOiJodHRwczovL2pvaG5vbWJ1eWEudXMuYXV0aDAuY29tLyIsInN1YiI6IjI3TkU3RU9BbGNNcklFUHMwZnVIV3I5cVptdGJBWlFUQGNsaWVudHMiLCJhdWQiOiJodHRwczovL3NhdmFubmFoLWluZm9ybWF0aWNzLWJhY2stZW5kLWNoYWxsZW5nZS5vbnJlbmRlci5jb20vYXBpIiwiaWF0IjoxNzI3MjMzOTgwLCJleHAiOjE3MjczMjAzODAsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IjI3TkU3RU9BbGNNcklFUHMwZnVIV3I5cVptdGJBWlFUIn0.VQtoUKZmaVXU8MZ-lrkJFhFeCOEOSJ9E1s3B5SfyRDtZ9zZT6_ZLA0MQY0w8RwrahYra9IT8Z0-s1_4zcOm9Yagj-EaVTknjF7Qwm6CiA_LozNX1TOOhyzudIarw5uiZ_nTdLJU84cUWbitAJSgd4pMenaqwCD4P9Np94GVqloFPNGTn71YbgrayE7VCNw1mxVyPfr3z1ewzS793hooz4ysN3BLiT2rjI3nf1uy4X1sdmMWmpIB3A-lblUnoPoRhEzhFiOuf0EVERdmLITWtsJmy8UXRgUc2_vIsFPkvCB-29YTn2mdxtmrav3X_VAM7uNtrmJrQ_z_3jlYCAC3ZiA" }

# conn.request("GET", "/api/orders", headers=headers)
conn.request("GET", "/api/orders")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

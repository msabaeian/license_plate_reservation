This script helps you to reserve a time for your car at License plate replacement center of Iran quickly.
# USE IT ON YOUR OWN RISK!

I'm not a python developer, I learn python in 2hours for this project so the code might smell (might? it must!)
<br/>

#### Module Installation
```
pip install -r requirements.txt
```
<br />

#### Usage
edit this section with your car and office details

```
main(
    sessId="u47416ovhco4l8bou8m2d2v7o3",
    user_id="3460297",
    office = "177842",
    service_type = ServiceType.Enteghal,
    pelak_type = CarType.SavariShakhsi,
    pelak_first = "47",
    pelak_middle = CarPelakType.V,
    pelak_last = "264",
    pelak_city_number = "34"
)
```

then run
```
python3 script.py
```
<br />

#### Info
find sessId (PHPSESSID) and user_id (epolicenopardaz_userid) in your browser cookie details and replace them
extract office code from the website: 
```
https://nobatdehi.epolice.ir/office/177842 => 177842
```

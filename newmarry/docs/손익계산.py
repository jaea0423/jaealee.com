import math
price=9900; ref=7900
pg=0.03
def net(p):
    vat=p/11
    fee=p*pg
    return p-vat-fee, vat, fee
for p in (price,ref):
    n,v,f=net(p); print(p, round(v), round(f), round(n))
fixed_m = 25*1400 + 30000/12   # Supabase Pro + domain
print('fixed/month', fixed_m, 'fixed/year', fixed_m*12)
n,_,_=net(price); nr,_,_=net(ref)
print('BEP/month (full price)', fixed_m/n, math.ceil(fixed_m/n))
print('BEP/month (all referral)', fixed_m/nr, math.ceil(fixed_m/nr))
# blended: 30% referral
bl=0.7*n+0.3*nr; print('blended net', round(bl), 'BEP', fixed_m/bl, math.ceil(fixed_m/bl))
print('annual BEP (blended)', math.ceil(fixed_m*12/bl))
# scenarios: annual bookings
mkt=222000
for name,cnt in (('보수',60),('기준',240),('낙관',720)):
    rev=cnt*(0.7*price+0.3*ref)
    netrev=cnt*bl
    print(name,cnt,'gross',round(rev),'net',round(netrev),'profit',round(netrev-fixed_m*12),'share %.3f%%'%(cnt/mkt*100))

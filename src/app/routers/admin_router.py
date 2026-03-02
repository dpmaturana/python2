from fastapi import APIRouter, HTTPException, Depends, Header

def verify_admin_key(api_key: str = Header()):
    if api_key != "eco-admin-secret":
        raise HTTPException(status_code=403, detail=f'Invalid API key: {api_key} not correct')

router = APIRouter(dependencies=[Depends(verify_admin_key)])

@router.get("/admin/stats")
def def_admin_stats():
    return {"users": 42, "bikes": 10, "rentals": 5}


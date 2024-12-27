from fastapi import FastAPI, Query, Body
import uvicorn


app = FastAPI(
    title="Momoa Web API",
)

hotels = [
    {"id": 1, "title": "Cesaes Side", "name": "nakamura property"},
    {"id": 2, "title": "The Grand Budapest Hotel", "name": "grand one"},
]
@app.get('/hotels')
def get_hotels(
        id: int | None = Query(None, description='Hotel ID'),
        title: str | None = Query(None, title="Hotel name"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


# body, request body
@app.post("/hotels")
def create_hotel(title: str = Body(embed=True, description='Hotel title')):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "ok"}


@app.put("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        new_title: str = Body(embed=True),
        new_name: str = Body(embed=True)
):
    global hotels
    try:
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                hotel['title'] = new_title
                hotel['name'] = new_name
                return {"status": "ok"}
        return {"status": "hotel not found"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.patch("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        new_title: str | None = Body(None, embed=True),
        new_name: str | None = Body(None, embed=True),
):
    if not new_title and not new_name:
        return {"status": "no params were given"}
    global hotels
    try:
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                if new_title:
                    hotel['title'] = new_title
                if new_name:
                    hotel['name'] = new_name
                return {"status": "ok"}
        return {"status": "hotel not found"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
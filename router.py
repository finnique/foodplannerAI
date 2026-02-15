def route_intent(state):
    intent = state.get("intent", "general_chat")

    if intent == "meal_plan":
        return "meal_planner"

    if intent == "update_preference":
        return "update_preference"

    if intent == "update_fridge":
        return "update_fridge"

    return "general_chat"


# from fastapi import APIRouter
# from app.schemas.chat import MealPlanRequest, InventoryItem
# from app.services.meal_planner import generate_dummy_meal_plan
# # from app.services.inventory import add_inventory, list_inventory

# router = APIRouter()

# # Meal planning endpoint
# @router.post("/plan_meal")
# async def plan_meal(request: MealPlanRequest):
#     return generate_dummy_meal_plan()

# # Inventory endpoints
# @router.post("/inventory/add")
# async def add_item(item: InventoryItem):
#     return add_inventory(item)

# @router.get("/inventory/list")
# async def get_inventory():
#     return list_inventory()

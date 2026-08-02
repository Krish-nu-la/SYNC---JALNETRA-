from app.services.risk_service import risk_service

tests = [3, 15, 35, 65]

for d in tests:

    print(risk_service.calculate(d))
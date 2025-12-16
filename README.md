Current stable API version: `v1` (unversioned path, assumed as v1).


## Domain Logic

- TimeSlot:
  - `TimeSlotQuerySet.future()` → همه‌ی slotهای آینده
  - `TimeSlotQuerySet.available()` → همه‌ی slotهایی که booking ندارند

- Booking:
  - `Booking.objects.create_booking(client, slot, notes)`:
    - جلوگیری از رزرو در گذشته
    - جلوگیری از رزرو دوباره‌ی یک slot
    - ساختن booking با status اولیه = PENDING

- Permissions:
  - `core.permissions.IsProvider` → نقش PROVIDER
  - `core.permissions.IsClient` → نقش CLIENT



## Running with Docker

Requirements:
- Docker
- Docker Compose

Steps:

```bash
cp .env.example .env  # edit values if needed
docker compose up --build
```

## Error Format

All errors returned by the API follow a consistent JSON structure:

- Validation errors (e.g. invalid input, slot already booked):

```json
{
  "errors": {
    "slot": ["This time slot is already booked."]
  }
}
```

## API Documentation

The API is documented using OpenAPI 3 via `drf-spectacular`.

Once the app is running (locally or via Docker), you can access:

- JSON schema: `GET /api/schema/`
- Swagger UI: `GET /api/docs/swagger/`
- Redoc UI: `GET /api/docs/redoc/`

Authentication:
- JWT-based (access and refresh tokens)
- Use `Authorization: Bearer <access_token>` header for protected endpoints.


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


## Service Layer

The project uses a service layer for business logic, separate from
Django views and serializers.

- `BookingService.create_booking(...)`  
  - Validates time slot  
  - Checks if already booked  
  - Enforces client role  
  - Saves the booking

- `BookingService.cancel_booking(...)`  
  - Ensures only client/provider can cancel  
  - Avoids double-cancellation  
  - Updates status safely

Views only orchestrate permissions and routing, while all business rules
live inside `services/`.

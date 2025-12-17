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

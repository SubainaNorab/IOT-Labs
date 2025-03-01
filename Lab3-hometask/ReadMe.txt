Task 3

1: What is a debounce issue and why we get rid of it?

A debounce issue occur when something runs too many  in short period. This can slow things down and cause unnecessary work. We get rid of it  because it can cause unnecessary repeated actions which can slow down performance, and overload the system with too many requests. Fixing it ensures smoother functionality, prevents extra work, and even improves user experience.


2:In which applications/domains, debounce issue can be threatening if not resolved in the system?

E-Commerce – Rapid clicks on "Buy Now" can result in multiple unintended orders, causing customer complaints and refunds.
Healthcare & Medical Devices – False triggers in medical sensors or duplicate patient entries can lead to incorrect diagnoses or treatments.
Automotive & Aerospace – Uncontrolled repeated signals in braking, acceleration, or flight controls can cause accidents.
Cybersecurity & Authentication – Multiple OTP or login requests can allow brute-force attacks or lock users out of their accounts.

3:Why debounce occurs? Is it a compiler error, logical error or micro-controller is cheap?

Debounce occurs due to logical errors. In software, rapid event triggers like button clicks or keystrokes cause unintended repeated actions.

It’s not a problem with the compiler or Micro controller. Even good microcontrollers can have this issue. To fix debounce , we use special coding techniques or electronic components to ensure only one action happens per press.

-----------------------------------------------------------------------------------------------------------------------------

Task 4

1:Why do we use interrupt?

We use interrupt to enable system to respond quickly to important events. In this way, we do not constantly check events in loop.Once the event is handled, the system resumes the task it was performing before the interruption.

2: How does interrupt lower the processing cost of the micro-controller?

Instead of continuously running code to detect changes , the microcontroller stays focused on its main task and only responds when an interrupt occurs. This helps to  save processing power, reduces energy consumption, and allow the system to handle multiple tasks efficiently. Once the interrupt is handled, the microcontroller go back to its previous task without wasting resources.

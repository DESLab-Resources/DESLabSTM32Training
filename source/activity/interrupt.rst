Interrupt
=========

MATERIALS
---------

1. STM32CubeIDE
2. `Grape32 Unleashed Kit – Grapestore (grapetech.vn) <UnleashedKit_>`_

   1. LEDs.
   2. BTN1.

ACTIVITY 1: EXTERNAL INTERRUPT
------------------------------

Using the external interrupt for BTN1, write a program that makes LED0 high when BTN1 is pushed and makes LED0 low when BTN1 is released.

ACTIVITY 2: SYSTEM TICK
-----------------------

Using the SysTick interrupt write a program that toggle LED0 four times a second.

ACTIVITY 3: TIM2
----------------

Rewrite the code of Activity 2 using TIM2.

ACTIVITY 4: TIM2 AND TIM3
-------------------------

Write a program that blinks LED2 twice a second and blinks LED3 three times a second. Use the TIM2 interrupt for LED2 and TIM3 for LED3.

ACTIVITY 5: TIMER AND EXTERNAL INTERRUPT
----------------------------------------

Using the external interrupt and the timer interrupt, write a program that when BTN1 is pushed, LED2 becomes high immediately and after 2 seconds LED3 becomes high. When BTN1 is released, both LEDs become low immediately.

Reference
---------

`STM32F103 Interrupt lab manual (nicerland.com) <https://nicerland.com/eduFiles/STM32F103/LabManuals/ch12_interrupt.pdf>`_

.. _UnleashedKit: https://store.grapetech.vn/product/bo-mach-vdk-grape32-unleashed-kit/

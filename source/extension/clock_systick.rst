System Clock Configuration
==========================

.. figure:: ../pics/W2_16-03-2024_15-20-51.png
   :align: center

   Clock Configuration: https://github.com/DESLab-Resources/DESLabSTM32Training_Systick/blob/ccb784819c21380f5a4e269d1f5dd399ef11ea93/Src/main.c#L66-L146

Configure SysTick control and status register (STK_CTRL)
--------------------------------------------------------

.. figure:: ../pics/W2_16-03-2024_15-39-42.png
   :align: center

   SysTick control and status register (STK_CTRL) (Source: \[[STM32_PM0056]_, page 151\])

.. code-block:: c

   // Bit 0 ENABLE: Counter enable
   // Bit 1 TICKINT: SysTick exception request enable
   SysTick->CTRL |= (0b11);
   // Bit 2 CLKSOURCE: Clock source selection
   SysTick->CTRL &= ~(1 << 2); // 0: AHB/8

Configure SysTick reload value register (STK_LOAD)
--------------------------------------------------

.. figure:: ../pics/W2_16-03-2024_15-43-42.png
   :align: center

   SysTick reload value register (STK_LOAD) (Source: \[[STM32_PM0056]_, page 152\])

.. code-block:: c

   // Bits 23:0 RELOAD[23:0]: RELOAD value
   SysTick->LOAD = 9000000-1; /* STRELOAD = (72,000,000/8)-1 */

Setup **SysTick_Handler**
-------------------------

.. code-block:: c

   void SysTick_Handler()
   {
         GPIOB->ODR ^= (1<<12); /* toggle PB12 */
   }

SysTick_Handler initialization
-------------------------------

**SysTick_Handler** is initialized in the file **startup_stm32f103rctx.s**.

.. code-block:: asm
   :linenos:
   :caption: /Startup/startup_stm32f103rctx.s

   // ...

   g_pfnVectors:
      .word	SysTick_Handler          			/* EXTI Line1 interrupt                             */

      // ...

      .weak	SysTick_Handler
      .thumb_set SysTick_Handler,Default_Handler

Full Implementation Source
--------------------------

.. code-block:: c
   :linenos:
   :emphasize-lines: 17-24, 30-33

   #include <stdint.h>
   #include <stm32f1xx.h>

   #if !defined(__SOFT_FP__) && defined(__ARM_FP)
   #warning "FPU is not initialized, but the project is compiling for an FPU. Please initialize the FPU before use."
   #endif

   void GPIO_Config (void);
   void ClockInit();

   int main(void)
   {
      SystemInit();
      GPIO_Config();
      ClockInit();

      // Bit 0 ENABLE: Counter enable
      // Bit 1 TICKINT: SysTick exception request enable
      SysTick->CTRL |= (0b11);
      // Bit 2 CLKSOURCE: Clock source selection
      SysTick->CTRL &= ~(1 << 2); // 0: AHB/8

      // Bits 23:0 RELOAD[23:0]: RELOAD value
      SysTick->LOAD = 9000000-1; /* STRELOAD = (72,000,000/8)-1 */

      /* Loop forever */
      for(;;);
   }

   void SysTick_Handler()
   {
         GPIOB->ODR ^= (1<<12); /* toggle PB12 */
   }

   void GPIO_Config (void)
   {
      // Set IOPB EN
      RCC->APB2ENR |= (1 << 3); // Enable GPIOB clock

      // Set MODE12[1:0] = 01: : Output mode, max speed 10 MHz
      GPIOB->CRH |= (1 << 16); // set bit 16
      GPIOB->CRH &= ~(1 << 17); // clear bit 17

      // Clear  CNF12[1:0]: General purpose output push-pull
      GPIOB->CRH &= ~(0b11 << 18);
   }

   void ClockInit(){
      // Bit 4 PRFTBE: Prefetch buffer enable
      FLASH->ACR |= (1 << 4); // Prefetch is enabled

      //
      // HSE Configuration
      // Bit 16 HSEON: HSE clock enable
      RCC->CR |= (1 << 16); // HSE oscillator ON

      /* Wait till HSE is ready */
      // Bit 17 HSERDY: External high-speed clock ready flag
      while(!(RCC->CR & (1 << 17)));

      //
      // PLL Configuration
      /* Disable the main PLL. */
      // Bit 24 PLLON: PLL enable
      RCC->CR &= ~(1 << 24); // PLL OFF

      /* Wait till PLL is disabled */
      // Bit 25 PLLRDY: PLL clock ready flag
      while(RCC->CR & (1 << 25));

      /* Set PREDIV1 Value */
      // Bit 17 PLLXTPRE: HSE divider for PLL entry
      RCC->CFGR &= ~(1 << 17); // HSE clock not divided

      /* Configure the main PLL clock source and multiplication factors. */
      // Bit 16 PLLSRC: PLL entry clock source
      RCC->CFGR |= (1 << 16); // HSE oscillator clock selected as PLL input clock
      // Bits 21:18 PLLMUL: PLL multiplication factor
      RCC->CFGR &= ~(0b1111 << 18);
      RCC->CFGR |= (0b111 << 18); // PLL input clock x 9

      /* Enable the main PLL. */
      // Bit 24 PLLON: PLL enable
      RCC->CR |= (1 << 24); // PLL ON

      /* Wait till PLL is ready */
      // Bit 25 PLLRDY: PLL clock ready flag
      while(!(RCC->CR & (1 << 25)));

      // Bits 2:0 LATENCY: Latency
      FLASH->ACR &= (0b111 << 0);
      FLASH->ACR |= (0b10 << 0); // Two wait states, if 48 MHz < SYSCLK <= 72 MHz

      // HCLK Configuration
      /* Set the highest APBx dividers in order to ensure that we do not go through
            5     a non-spec phase whatever we decrease or increase HCLK. */
      // Bits 10:8 PPRE1: APB low-speed prescaler (APB1)
      RCC->CFGR |= (0b111 << 8); // HCLK divided by 16
      // Bits 13:11 PPRE2: APB high-speed prescaler (APB2)
      RCC->CFGR |= (0b111 << 11); // HCLK divided by 16

      /* Set the new HCLK clock divider */
      // Bits 7:4 HPRE: AHB prescaler
      RCC->CFGR &= ~(0b1111 << 4); // SYSCLK not divided

      //
      // SYSCLK Configuration
      /* PLL is selected as System Clock Source */
      // Bit 25 PLLRDY: PLL clock ready flag
      /* Check the PLL ready flag */
      while(!(RCC->CR & (1 << 25)));

      // Bits 1:0 SW: System clock switch
      RCC->CFGR &= ~(1 << 0); // PLL selected as system clock
      RCC->CFGR |= (1 << 1);

      while( ( ( RCC->CFGR & (0b11 << 2) ) >> 2 ) != (0b10) ); // Bits 3:2 SWS: System clock switch status

      //
      // PCLK1 Configuration
      // Bits 10:8 PPRE1: APB low-speed prescaler (APB1)
      RCC->CFGR &= ~(0b111 << 8);
      RCC->CFGR |= (0b100 << 8); // HCLK divided by 2

      // PCLK2 Configuration
      // Bits 13:11 PPRE2: APB high-speed prescaler (APB2)
      RCC->CFGR &= ~(0b111 << 11); // HCLK not divided
   }

Reference
---------

1. https://nicerland.com/eduFiles/STM32F103/PPts/12_Interrupt.pps


.. [STM32_PM0056] https://www.st.com/resource/en/programming_manual/pm0056-stm32f10xxx20xxx21xxxl1xxxx-cortexm3-programming-manual-stmicroelectronics.pdf

#ifndef __BOARD_H__
#define __BOARD_H__

#if !defined(BOARD)
# error Preprocessor directive 'BOARD' not specified. Stop.
#endif

#define stm32f0discovery	0x01

#if (BOARD == stm32f0discovery)

# define LED_CLOCK	RCC_GPIOC
# define LED_PORT	GPIOC
# define LED_PIN	GPIO8

#else

# error Unsupported board! Stop.

#endif

#endif /* __BOARD_H__ */
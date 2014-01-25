#ifndef __STM32F0DISCOVERY_H__
#define __STM32F0DISCOVERY_H__

#define BOARD_NAME		"STM32F0-Discovery"

/******************************************************************************
 * LED configuration
 ******************************************************************************/

struct pin_config board_leds[] = {
	{	/* Blue LED */
		.port = GPIOC,
		.pin = GPIO8,
		.clock = RCC_GPIOC,
	} , {	/* Green LED */
		.port = GPIOC,
		.pin = GPIO9,
		.clock = RCC_GPIOC,
	}
};

#define BOARD_NLEDS	sizeof(board_leds) / sizeof(struct pin_config)

#define BOARD_LED_GREEN		1
#define BOARD_LED_BLUE		0

/******************************************************************************
 * Serial port configuration
 ******************************************************************************/


#endif /* __STM32F0DISCOVERY_H__ */
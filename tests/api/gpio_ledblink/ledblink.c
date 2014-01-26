/*
 * This file is part of the libopencm3 project.
 *
 * Copyright (C) 2014 Frantisek Burian <BuFran@seznam.cz>
 *
 * This library is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include "board.h"

static void delay(int clocks)
{
	int i;
	for (i = 0; i < clocks; i++)
		__asm__ __volatile__ ("nop");
}

int main(void)
{
	uint32_t i;

	/* Initialize all LED's */
	for (i = 0; i < BOARD_NLEDS; i++) {

		/* Enable the clocks for the port of specified LED */
		rcc_periph_clock_enable(board_leds[i].clock);

#if defined(STM32F1)
		/* Set the LED pin to the output */
		gpio_set_mode(board_leds[i].port,
				GPIO_MODE_OUTPUT_50_MHZ,
				GPIO_CNF_OUTPUT_PUSHPULL,
				board_leds[i].pin);
#else
		/* Set the LED pin to the output */
		gpio_mode_setup(board_leds[i].port,
				GPIO_MODE_OUTPUT,
				GPIO_PUPD_NONE,
				board_leds[i].pin);
#endif
	}

	while (1) {
		/* Toggle all leds on the board */
		for (i = 0; i < BOARD_NLEDS; i++) {
			gpio_toggle(board_leds[i].port, board_leds[i].pin);
		}

		/* loop some clocks to slow down the blinking */
		delay(1000000);
	}
}
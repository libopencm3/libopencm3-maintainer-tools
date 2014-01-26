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
#include <libopencm3/stm32/usart.h>
#include "board.h"

/******************************************************************************
 * LED configuration
 ******************************************************************************/

struct pin_config board_leds[] = {
	{	/* Blue LED LD6 */
		.port = GPIOD,
		.pin = GPIO15,
		.clock = RCC_GPIOD,
	} , {	/* Green LED LD4 */
		.port = GPIOD,
		.pin = GPIO12,
		.clock = RCC_GPIOD,
	} , {	/* Orange LED LD3 */
		.port = GPIOD,
		.pin = GPIO13,
		.clock = RCC_GPIOD,
	} , {	/* Red LED LD5 */
		.port = GPIOD,
		.pin = GPIO14,
		.clock = RCC_GPIOD,
	}
};

/******************************************************************************
 * BUTTON configuration
 ******************************************************************************/

struct pin_config board_btns[] = {
	{	/* USER KEY */
		.port = GPIOA,
		.pin = GPIO0,
		.clock = RCC_GPIOA,
	}
};

/******************************************************************************
 * Serial port configuration
 ******************************************************************************/

struct usart_config board_usarts[] = {
};
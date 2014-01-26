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
	{
		.port = USART1,
		.clock = RCC_USART1,
		.af = GPIO_AF1,
		.rxpin = {
			.port = GPIOA,
			.pin = GPIO10,
			.clock = RCC_GPIOA,
		},
		.txpin = {
			.port = GPIOA,
			.pin = GPIO9,
			.clock = RCC_GPIOA,
		},
	}
};
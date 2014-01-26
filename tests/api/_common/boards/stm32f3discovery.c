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
	{	/* LD4 Blue */
		.port = GPIOE,
		.pin = GPIO8,
		.clock = RCC_GPIOE,
	} , {	/* LD6 Green */
		.port = GPIOE,
		.pin = GPIO15,
		.clock = RCC_GPIOE,
	} , {	/* LD5 Orange */
		.port = GPIOE,
		.pin = GPIO10,
		.clock = RCC_GPIOE,
	} , {	/* LD3 Red */
		.port = GPIOE,
		.pin = GPIO9,
		.clock = RCC_GPIOE,
	} , {	/* LD7 Green */
		.port = GPIOE,
		.pin = GPIO11,
		.clock = RCC_GPIOE,
	} , {	/* LD8 Orange */
		.port = GPIOE,
		.pin = GPIO14,
		.clock = RCC_GPIOE,
	} , {	/* LD9 Blue */
		.port = GPIOE,
		.pin = GPIO12,
		.clock = RCC_GPIOE,
	} , {	/* LD10 Red */
		.port = GPIOE,
		.pin = GPIO13,
		.clock = RCC_GPIOE,
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
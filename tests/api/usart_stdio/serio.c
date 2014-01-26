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

#include <stdio.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>
#include "board.h"
#include "serio.h"

#define UNUSED __attribute__ ((unused))

static ssize_t serio_iord(void *_cookie UNUSED, char *_buf UNUSED, size_t _n UNUSED)
{
	/* dont support reading now */
	return 0;
}

static ssize_t serio_iowr(void *_cookie, const char *_buf, size_t _n)
{
	struct usart_config *uc = (struct usart_config *)_cookie;

	int written = 0;
	while (_n-- > 0) {
		usart_send_blocking(uc->port, *_buf++);
		written++;
	};
	return written;
}

cookie_io_functions_t serio_cookie = { serio_iord, serio_iowr, NULL, NULL };



FILE *serio_init(struct usart_config *uc)
{
	FILE *fp;

	/* Enable the clocks for the module */
	rcc_periph_clock_enable(uc->clock);
	rcc_periph_clock_enable(uc->rxpin.clock);
	rcc_periph_clock_enable(uc->txpin.clock);

	/* Set pin configuration for USART pins */
#if defined(STM32F1)
#else
	gpio_mode_setup(uc->txpin.port,
		GPIO_MODE_AF,
		GPIO_PUPD_NONE,
		uc->txpin.pin);
	gpio_mode_setup(uc->rxpin.port,
		GPIO_MODE_AF,
		GPIO_PUPD_PULLUP,
		uc->rxpin.pin);
	
	gpio_set_af(uc->txpin.port, uc->af, uc->txpin.pin);
	gpio_set_af(uc->rxpin.port, uc->af, uc->rxpin.pin);
#endif

	/* Set port configuration */
	usart_set_baudrate(uc->port, 38400);
	usart_set_databits(uc->port, 8);
	usart_set_parity(uc->port, USART_PARITY_NONE);
	usart_set_stopbits(uc->port, USART_CR2_STOP_1_0BIT);
	usart_set_mode(uc->port, USART_MODE_TX_RX);
	usart_set_flow_control(uc->port, USART_FLOWCONTROL_NONE);

	usart_enable(uc->port);

	fp = fopencookie(uc, "rw+", serio_cookie);

	setvbuf(fp, NULL, _IONBF, 0);
	return fp;
}
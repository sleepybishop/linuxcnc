//
// This is a userspace HAL driver for the Semtech SX1509B
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301-1307 USA
//


#include <errno.h>
#include <fcntl.h>
#include <glob.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/ioctl.h>
#include <sys/stat.h>
#include <sys/types.h>

#include "i2c.h"
#include "hal.h"

#define MAX_PINS (16)

#define SX1509B_ADDR (0x3E)

#define SX1509_REG_INPUTDISABLE    (0x00)
#define SX1509_REG_PULLUP          (0x06)
#define SX1509_REG_PULLDOWN        (0x08)
#define SX1509_REG_OPENDRAIN       (0x0A)
#define SX1509_REG_POLARITY        (0x0C)
#define SX1509_REG_DIR             (0x0E)
#define SX1509_REG_DATA            (0x10)
#define SX1509_REG_CLOCK           (0x1E)
#define SX1509_REG_MISC            (0x1F)
#define SX1509_REG_LEDDRIVERENABLE (0x20)
#define SX1509_REG_DEBOUNCECFG     (0x22)
#define SX1509_REG_DEBOUNCEENABLE  (0x23)
#define SX1509_REG_RESET           (0x7D)

/* Register map for the Intensity setting (per pin) */
static uint8_t reg_intensity[] = {
  0x2A, 0x2D, 0x30, 0x33, 0x36, 0x3B, 0x40, 0x45, \
    0x4A, 0x4D, 0x50, 0x53, 0x56, 0x5B, 0x60, 0x65} ;


// the module name, and prefix for all HAL pins
char *modname = "sx1509b";

int hal_comp_id;

// each sx1509b device presents this interface to HAL
struct sx1509b_hal {
  hal_bit_t *gpio[MAX_PINS];
  hal_float_t *pwm[MAX_PINS];  // pwm intensity for pins configured as such
  hal_u32_t *config;           // pin config
};

struct sx1509b {
  int fd;
  char *device_file;
  struct sx1509b_hal *hal;
  uint32_t prev_config;
};

// this will become an array of all the SX1509b devices we're using
struct sx1509b **sx1509b = NULL;
int num_devices = 0;
int should_exit = 0;
static void exit_handler(int sig) {
  should_exit = 1;
}

static void call_hal_exit(void) {
  hal_exit(hal_comp_id);
}

static int setup_pins(struct sx1509b *s) {
  uint32_t bcfg1 = ((*s->hal->config) >> 0) & 0xff;
  uint32_t bcfg0 = ((*s->hal->config) >> 8) & 0xff;

  i2c_writereg(s->fd, SX1509_REG_LEDDRIVERENABLE + 1, bcfg1);
  i2c_writereg(s->fd, SX1509_REG_LEDDRIVERENABLE + 0, bcfg0);

  i2c_writereg(s->fd, SX1509_REG_INPUTDISABLE + 1, bcfg1);
  i2c_writereg(s->fd, SX1509_REG_INPUTDISABLE + 0, bcfg0);

  i2c_writereg(s->fd, SX1509_REG_DIR + 1, ~bcfg1);
  i2c_writereg(s->fd, SX1509_REG_DIR + 0, ~bcfg0);

  i2c_writereg(s->fd, SX1509_REG_DATA + 1, ~bcfg1);
  i2c_writereg(s->fd, SX1509_REG_DATA + 0, ~bcfg0);

  i2c_writereg(s->fd, SX1509_REG_PULLUP + 1, ~bcfg1);
  i2c_writereg(s->fd, SX1509_REG_PULLUP + 0, ~bcfg0);

  i2c_writereg(s->fd, SX1509_REG_DEBOUNCEENABLE + 1, ~bcfg1);
  i2c_writereg(s->fd, SX1509_REG_DEBOUNCEENABLE + 0, ~bcfg0);

  s->prev_config = *s->hal->config;
}

static int read_update(struct sx1509b *s) {
  int r;

  if (*s->hal->config != s->prev_config) {
    setup_pins(s);
  }

  uint32_t bcfg1 = ((*s->hal->config) >> 0) & 0xff;
  uint32_t bcfg0 = ((*s->hal->config) >> 8) & 0xff;

  uint8_t data1 = i2c_readreg(s->fd, SX1509_REG_DATA + 1);
  uint8_t data0 = i2c_readreg(s->fd, SX1509_REG_DATA + 0);

  for (int i = 0; i < MAX_PINS; i++) {
    if ((*s->hal->config & (1 << i)) == 0) {
      if (i > 7) {
        *s->hal->gpio[i] = (data0 & (1 << (i % 8))) == 0;
      } else {
        *s->hal->gpio[i] = (data1 & (1 << (i % 8))) == 0;
      }
    } else {
      float val = *s->hal->pwm[i];
      if (val < 0) val = 0.0;
      if (val > 100) val = 100.0;
      val = 100.0 - val;
      uint8_t tmp = (uint8_t)(255.0*val/100.0);
      i2c_writereg(s->fd, reg_intensity[i], tmp);
      *s->hal->gpio[i] = tmp == 0;
    }
  }

  return 0;
}

struct sx1509b *check_for_sx1509b(char *dev_filename) {
  struct sx1509b *s;
  char name[100];
  int r;

  //printf("%s: checking %s\n", modname, dev_filename);

  s = (struct sx1509b *)calloc(1, sizeof(struct sx1509b));
  if (s == NULL) {
    fprintf(stderr, "%s: out of memory!\n", modname);
    return NULL;
  }

  s->device_file = dev_filename;

  s->fd = i2c_open(dev_filename, SX1509B_ADDR);

  s->prev_config = 0;

  if (s->fd < 0) {
    fprintf(stderr, "%s: error opening %s: %s\n", modname, s->device_file, strerror(errno));
    if (errno == EACCES) {
      fprintf(stderr, "%s: make sure you have read permission on %s\n", modname, s->device_file);
    }
    goto fail0;
  }

  //printf("%s: found %s on %s\n", modname, name, s->device_file);

  s->hal = (struct sx1509b_hal *)hal_malloc(sizeof(struct sx1509b_hal));
  if (s->hal == NULL) {
    fprintf(stderr, "%s: ERROR: unable to allocate HAL shared memory\n", modname);
    goto fail1;
  }

  // soft reset
  i2c_writereg(s->fd, SX1509_REG_RESET, 0x12);
  i2c_writereg(s->fd, SX1509_REG_RESET, 0x34);

  // setup clock
  i2c_writereg(s->fd, SX1509_REG_CLOCK, 0b01000000); // internal 1mhz

  // setup pwm frequency
  i2c_writereg(s->fd, SX1509_REG_MISC, 0x40);

  // setup debounce (16ms)
  i2c_writereg(s->fd, SX1509_REG_DEBOUNCECFG, 0b00000101); 

  r = hal_pin_u32_newf(HAL_IN, &(s->hal->config), hal_comp_id, "%s.%d.config", modname, num_devices);
  if (r != 0) goto fail1;
  *s->hal->config = 0;

  for (int i = 0; i < MAX_PINS; i++) {
    r = hal_pin_bit_newf(HAL_IN | HAL_OUT, &(s->hal->gpio[i]), hal_comp_id, "%s.%d.gpio-%02d", modname, num_devices, i);
    if (r != 0) goto fail1;
    *s->hal->gpio[i] = 0;

    r = hal_pin_float_newf(HAL_IN, &(s->hal->pwm[i]), hal_comp_id, "%s.%d.pwm-%02d", modname, num_devices, i);
    if (r != 0) goto fail1;
    *s->hal->pwm[i] = 0.0;
  }

  return s;

fail1:
  i2c_close(s->fd);

fail0:
  free(s);
  return NULL;
}

int main(int argc, char *argv[]) {
  int i;
  glob_t glob_buffer;

  char **names;
  int num_names;

  hal_comp_id = hal_init(modname);
  if (hal_comp_id < 1) {
    fprintf(stderr, "%s: ERROR: hal_init failed\n", modname);
    exit(1);
  }

  signal(SIGINT, exit_handler);
  signal(SIGTERM, exit_handler);
  atexit(call_hal_exit);

  // get the list of device filenames to check for SX1509b's
  if (argc > 1) {
    // list of devices provided on the command line
    names = &argv[1];
    num_names = argc - 1;
  } else {
    int r;

    r = glob("/dev/i2c*", 0, NULL, &glob_buffer);
    if (r == GLOB_NOMATCH) {
      fprintf(stderr, "%s: no /dev/i2c* found, is device powered?\n", modname);
      exit(1);
    } else if (r != 0) {
      fprintf(stderr, "%s: error with glob!\n", modname);
      exit(1);
    }
    names = glob_buffer.gl_pathv;
    num_names = glob_buffer.gl_pathc;

    // the pathnames we got from glob(3) are used in the sx1509b array, so we intentionally dont call globfree(3)
  }

  // probe for sx1509b devices on all those device file names
  for (i = 0; i < num_names; i ++) {
    struct sx1509b *s;
    s = check_for_sx1509b(names[i]);
    if (s == NULL) continue;

    num_devices ++;
    sx1509b = (struct sx1509b **)realloc(sx1509b, (num_devices * sizeof(struct sx1509b *)));
    if (sx1509b == NULL) {
      fprintf(stderr, "%s: out of memory!\n", modname);
      exit(1);
    }
    sx1509b[num_devices - 1] = s;
  }

  if (num_devices == 0) {
    fprintf(stderr, "%s: no devices found\n", modname);
    exit(1);
  }

  hal_ready(hal_comp_id);

  while(!should_exit) {
    for(i = 0; i < num_devices; i++) {
      read_update(sx1509b[i]);
    }
    usleep(250000);
  }

  for(i = 0; i < num_devices; i++) {
    i2c_writereg(sx1509b[i]->fd, SX1509_REG_RESET, 0x12);
    i2c_writereg(sx1509b[i]->fd, SX1509_REG_RESET, 0x34);
    i2c_close(sx1509b[i]->fd);
  }
  exit(0);
}


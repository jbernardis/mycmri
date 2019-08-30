	def poll(self):
		self.bus.write(b'\xFF')
		self.bus.write(b'\xFF')
		self.bus.write(STX)
		self.bus.write(bytes([65 + self.addr]))
		self.bus.write(POLL)
		self.bus.write(ETX)
		self.bus.flush()

		self.newInBuffer = []
		c = b'\xFF'
		while c == b'\xFF':
			c = self.bus.read()
			if len(c) == 0:
				raise CMRI_READ_EXCEPTION

		if c != STX:
			raise CMRI_READ_EXCEPTION

		addr = self.bus.read()
		if len(addr) == 0:
			raise CMRI_READ_EXCEPTION
		if addr != bytes([65 + self.addr]):  #elf.addr:
			raise CMRI_ADDRESS_EXCEPTION(addr, self.addr)
		cmd = self.bus.read()
		if len(cmd) == 0:
			raise CMRI_READ_EXCEPTION
		if cmd != GET:
			raise CMRI_COMMAND_EXCEPTION(cmd)
		c = self.bus.read()
		if len(c) == 0:
			raise CMRI_READ_EXCEPTION
		while c != ETX:
			if c == ESC or c == ETX:
				c = self.bus.read()
			self.newInBuffer.append(ord(c))
			c = self.bus.read()
			if len(c) == 0:
				raise CMRI_READ_EXCEPTION

		s = "in buffer: "
		for b in self.newInBuffer:
			s += ("%02x " % b)
		print(s)

		if len(self.newInBuffer) != len(self.inBuffer):
			raise CMRI_READ_EXCEPTION

		else:
			offset = 0
			for old, new in zip(self.inBuffer, self.newInBuffer):
				if new != old:
					for b in range(BITS_PER_BYTE):
						o = old & (1 << BITS_PER_BYTE-1-b)
						n = new & (1 << BITS_PER_BYTE-1-b)
						if n != 0:
							nv = 1
						else:
							nv = 0
						if o != n:
							self.cb(b+offset, nv)
				offset += BITS_PER_BYTE

			self.inBuffer = [x for x in self.newInBuffer]

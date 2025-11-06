class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text_surface = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text_surface
		self.image_rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
		self.text_rect = self.text_surface.get_rect(center = (self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.image_rect)
		screen.blit(self.text_surface, self.text_rect)

	def check_for_input(self, position):
		if (position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in
                range(self.text_rect.top, self.text_rect.bottom)):
			return True
		return False

	def change_color(self, position):
		if (position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in
                range(self.text_rect.top, self.text_rect.bottom)):
			self.text_surface = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text_surface = self.font.render(self.text_input, True, self.base_color)
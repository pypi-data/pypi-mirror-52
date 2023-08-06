#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for legend drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.fill_color = pero.colors.Ivory
        canvas.fill()
        
        # init coords
        padding = 20
        width, height = canvas.viewport.wh
        
        # init legend items
        legend1 = pero.MarkerLegend(
            text = "First legend",
            marker = "o",
            marker_line_color = pero.colors.Blue,
            marker_fill_color = pero.colors.Blue.lighter(.2))
        
        legend2 = pero.MarkerLegend(
            text = "Second legend\nwith two lines",
            marker = "x",
            marker_line_color = pero.colors.Green,
            marker_fill_color = pero.colors.Green.lighter(.2))
        
        legend3 = pero.MarkerLegend(
            text = "Third legend",
            marker = "s",
            marker_line_color = pero.colors.Red,
            marker_fill_color = pero.colors.Red.lighter(.2))
        
        # init legend
        legend = pero.Legends(
            items = (legend1, legend2, legend3),
            orientation = pero.VERTICAL)
        
        # draw nw
        legend.draw(canvas,
            x = padding,
            y = padding,
            anchor = pero.POSITION.NW)
        
        # draw n
        legend.draw(canvas,
            x = 0.5*width,
            y = padding,
            anchor = pero.POSITION.N)
        
        # draw ne
        legend.draw(canvas,
            x = width-padding,
            y = padding,
            anchor = pero.POSITION.NE)
        
        # draw e
        legend.draw(canvas,
            x = width-padding,
            y = 0.5*height,
            anchor = pero.POSITION.E)
        
        # draw se
        legend.draw(canvas,
            x = width-padding,
            y = height-padding,
            anchor = pero.POSITION.SE)
        
        # draw s
        legend.draw(canvas,
            x = 0.5*width,
            y = height-padding,
            anchor = pero.POSITION.S)
        
        # draw sw
        legend.draw(canvas,
            x = padding,
            y = height-padding,
            anchor = pero.POSITION.SW)
        
        # draw w
        legend.draw(canvas,
            x = padding,
            y = 0.5*height,
            anchor = pero.POSITION.W)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'qt', "Legend", 500, 350)

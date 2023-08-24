import pcbnew
import FootprintWizardBase
import math
from PadArray import PadMaker


class FluxNeutralCoilGen(FootprintWizardBase.FootprintWizard):
    GetName = lambda self: 'Flux Neutral Coil Generator'
    GetDescription = lambda self: 'Generates a flux-neutral coil within a circular aperture.'
    GetValue = lambda self: 'temporary_name'

    center_x = 0
    center_y = 0

    def GenerateParameterList(self):
        # Information about where this footprint needs to fit into.
        self.AddParam("Install Info", "Outer Ring radius", self.uMM, 75)
        self.AddParam("Install Info", "Outer Ring gap", self.uMM, 2)

        # Info about the fabrication capabilities
        self.AddParam("Fab Specs", "trace_width", self.uMM, 0.2)
        self.AddParam("Fab Specs", "trace_spacing", self.uMM, 0.2)
        self.AddParam("Fab Specs", "via_drill", self.uMM, 0.254)        # 0.010"
        self.AddParam("Fab Specs", "via_annular_ring", self.uMM, 0.127) # 0.005"

        # Info about the coil itself.  
        self.AddParam("Coil specs", "turns", self.uInteger, 5)
        self.AddParam("Coil specs", "Minimum_Radius", self.uMM, 1)

    def CheckParameters(self):
        self.aperture_r = self.parameters['Install Info']['Outer Ring radius']
        self.aperture_gap = self.parameters['Install Info']['Outer Ring gap']
        
        self.trace_width = self.parameters['Fab Specs']['trace_width']
        self.trace_space = self.parameters['Fab Specs']['trace_spacing']
        self.via_hole = self.parameters['Fab Specs']['via_drill']
        self.via_ann_ring = self.parameters['Fab Specs']['via_annular_ring']

        self.turns = self.parameters['Coil specs']['turns']
        self.min_radius = self.parameters['Coil specs']['Minimum_Radius']
        
    def BuildThisFootprint(self):
        t_size = self.GetTextSize()
        self.draw.SetLayer(pcbnew.User_1)
        self.draw.Circle(self.center_x, self.center_y, self.aperture_r)
        pitch = self.trace_space + self.trace_width/2 + max(self.trace_width/2, self.via_hole/2 + self.via_ann_ring)

        # Pythagorean Theorum to determine via spacing
        aa = self.via_hole/2 + self.via_ann_ring + self.trace_space + self.trace_width/2
        cc = self.via_ann_ring*2 + self.via_hole + self.trace_space
        via_gap = math.sqrt(cc * cc - aa * aa)  #units of KiCAD_internal
        
        self.draw.SetLineThickness(self.trace_width)

        
        # Draw large curves
        arc_center_x = self.center_x - pitch*(self.turns-1)/2 - self.min_radius - via_gap
        arc_center_y = self.center_y
        arc_start_x = arc_center_x
        arc_start_y = arc_center_y + self.aperture_r - self.aperture_gap - pitch*(self.turns-1)/2 - self.min_radius - via_gap
        for ii in range(self.turns):
            self.draw.SetLayer(pcbnew.F_Cu)
            self.draw.Arc(arc_center_x, arc_center_y,
                          arc_start_x,  arc_start_y - ii*pitch ,    
                          pcbnew.EDA_ANGLE( 180, pcbnew.DEGREES_T ) )
            self.draw.SetLayer(pcbnew.B_Cu)
            self.draw.Arc(- arc_center_x, -arc_center_y,
                          - arc_start_x,  -arc_start_y + ii*pitch ,
                          pcbnew.EDA_ANGLE( 180, pcbnew.DEGREES_T ) )

        # Draw verticals
        start_x = (self.turns - 1) / 2 * pitch
        self.draw.SetLayer(pcbnew.F_Cu)
        line_length = self.center_y + self.aperture_r - self.aperture_gap - pitch*(self.turns-1)*1.5 - self.min_radius*2 - via_gap
        for ii in range(self.turns-1):
            self.draw.Line(start_x - ii*pitch,  line_length,
                           start_x - ii*pitch, -line_length)
        self.draw.Line(-start_x,  line_length, 
                       -start_x, -line_length + pcbnew.FromMM(10)) #Stub to breakout to tap point

        self.draw.SetLayer(pcbnew.B_Cu)
        for ii in range(self.turns):
            self.draw.Line(start_x - ii*pitch,  line_length,     
                           start_x - ii*pitch, -line_length)


        # Draw small curves
        small_arc_center_x = (self.turns - 1) / 2 * pitch + self.min_radius
        small_arc_center_y = self.center_y + self.aperture_r - self.aperture_gap - pitch*(self.turns-1)*1.5 - self.min_radius*2 - via_gap

        self.draw.SetLayer(pcbnew.F_Cu)
        for ii in range(self.turns):
            if (  (ii != 0) or (self.min_radius != 0  ) ):       # Checking for a radius=0 arc. Might be overkill....
                self.draw.Arc(small_arc_center_x,                              small_arc_center_y, 
                              small_arc_center_x - self.min_radius - ii*pitch, small_arc_center_y, 
                              pcbnew.EDA_ANGLE( -90, pcbnew.DEGREES_T ))
        
        for ii in range(self.turns):   
            if (  (ii != 0)):       # Checking for a radius=0 arc. Might be overkill....
                self.draw.Arc(-small_arc_center_x + pitch,                      -small_arc_center_y, 
                              -small_arc_center_x + self.min_radius + ii*pitch, -small_arc_center_y, 
                              pcbnew.EDA_ANGLE( -90, pcbnew.DEGREES_T ))
        

        self.draw.SetLayer(pcbnew.B_Cu)
        for ii in range(self.turns):
            if (  (ii != 0) or (self.min_radius != 0  ) ):       # Checking for a radius=0 arc. Might be overkill....
                self.draw.Arc(-small_arc_center_x,                              small_arc_center_y, 
                              -small_arc_center_x + self.min_radius + ii*pitch, small_arc_center_y, 
                              pcbnew.EDA_ANGLE( 90, pcbnew.DEGREES_T ))
                
        for ii in range(self.turns):
            if (  (ii != 0) or (self.min_radius != 0  ) ):       # Checking for a radius=0 arc. Might be overkill....
                self.draw.Arc(small_arc_center_x,                              -small_arc_center_y, 
                              small_arc_center_x - self.min_radius - ii*pitch, -small_arc_center_y, 
                              pcbnew.EDA_ANGLE( 90, pcbnew.DEGREES_T ))


        # Draw simple Horizontal Lines

        self.draw.SetLayer(pcbnew.B_Cu)
        for ii in range (self.turns):
            self.draw.Line(-arc_start_x,           -arc_start_y + ii*pitch,
                           -arc_start_x - via_gap, -arc_start_y + ii*pitch)
        self.draw.SetLayer(pcbnew.F_Cu) 
        for ii in range (1, self.turns):
            self.draw.Line(arc_start_x,                   -arc_start_y + ii*pitch,
                           arc_start_x + via_gap + pitch, -arc_start_y + ii*pitch)
            
        # Draw alternating Horizontal Lines for Vias
        
        for ii in range (self.turns):
            if ((ii % 2)==1):
                self.draw.SetLayer(pcbnew.F_Cu) 
            else:
                self.draw.SetLayer(pcbnew.B_Cu)
            self.draw.Line(arc_start_x,           arc_start_y - ii*pitch,
                           arc_start_x + via_gap, arc_start_y - ii*pitch)
            
            if ((ii % 2)==1):
                self.draw.SetLayer(pcbnew.B_Cu) 
            else:
                self.draw.SetLayer(pcbnew.F_Cu)
            
            self.draw.Line(-arc_start_x,           arc_start_y - ii*pitch,
                           -arc_start_x - via_gap, arc_start_y - ii*pitch)

        # Draw Vias
        via_d = self.via_ann_ring*2 + self.via_hole
        pad = pcbnew.PAD(self.module)
        pad.SetSize(pcbnew.VECTOR2I(via_d,via_d))
        pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        pad.SetLayerSet(pad.PTHMask())
        pad.SetDrillSize(pcbnew.VECTOR2I(self.via_hole, self.via_hole))

        for ii in range(self.turns):
            if ((ii % 2)==1):
                offset = via_gap
            else:
                offset = 0
            pos = pcbnew.VECTOR2I(int(arc_start_x + offset),
                                  int(arc_start_y - ii*pitch))
            pad.SetPosition(pos)
            pad.SetPos0(pos)
            self.module.Add(pad)
            pad = pad.Duplicate()

            pos = pcbnew.VECTOR2I(int(-arc_start_x - offset),
                                  int(arc_start_y - ii*pitch))
            pad.SetPosition(pos)
            pad.SetPos0(pos)
            self.module.Add(pad)
            pad = pad.Duplicate()

        # Draw tap points



<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>
<sld:StyledLayerDescriptor version="1.0.0" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink">

  <sld:NamedLayer>
    <sld:Name>3Zona</sld:Name>
    <sld:UserStyle>
      <sld:Name>Style1</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:FeatureTypeName>3Zona</sld:FeatureTypeName>
        <sld:Rule>
          <sld:Name>Origen Nacional</sld:Name>
          <sld:Title>Origen Nacional</sld:Title>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>Zona</ogc:PropertyName>
              <ogc:Literal>Origen Nacional</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <sld:PolygonSymbolizer>
            <sld:Fill>
              <sld:CssParameter name="fill">#ffffff</sld:CssParameter>
              <sld:CssParameter name="fill-opacity">0.1</sld:CssParameter>
            </sld:Fill>
          </sld:PolygonSymbolizer>
		 <TextSymbolizer>
	     <Label>
              <ogc:PropertyName>Zona</ogc:PropertyName>
         </Label>
            <Font>
	      <CssParameter name="font-family">Arial</CssParameter>
	      <CssParameter name="font-size">10</CssParameter>
	      <CssParameter name="font-style">normal</CssParameter>
	      <CssParameter name="font-weight">normal</CssParameter>
            </Font>
			<sld:Fill>
              <sld:CssParameter name="fill">#002673</sld:CssParameter>
              <sld:CssParameter name="fill-opacity">1.0</sld:CssParameter>
            </sld:Fill>
	     <LabelPlacement>
           <PointPlacement>
             <AnchorPoint>
               <AnchorPointX>0</AnchorPointX>
               <AnchorPointY>0</AnchorPointY>
             </AnchorPoint>
			 <Rotation>0</Rotation>
             <Displacement>
               <DisplacementX>-35</DisplacementX>
               <DisplacementY>190</DisplacementY>
             </Displacement>
           </PointPlacement>
         </LabelPlacement>	
         </TextSymbolizer>		 
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>
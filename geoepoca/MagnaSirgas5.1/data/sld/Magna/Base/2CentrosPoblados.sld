<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<sld:StyledLayerDescriptor version="1.0.0" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink">
  <sld:NamedLayer>
    <sld:Name>2CentrosPoblados</sld:Name>
    <sld:UserStyle>
      <sld:Name>Style1</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:FeatureTypeName>2CentrosPoblados</sld:FeatureTypeName>
        <sld:Rule>
          <sld:Name>2CentrosPoblados</sld:Name>
          <sld:Title>2CentrosPoblados</sld:Title>
          <sld:PolygonSymbolizer>
            <sld:Fill>
              <sld:CssParameter name="fill">#6871ed</sld:CssParameter>
              <sld:CssParameter name="fill-opacity">0.3</sld:CssParameter>
            </sld:Fill>
            <sld:Stroke>
              <sld:CssParameter name="stroke">#6871ed</sld:CssParameter>
              <sld:CssParameter name="stroke-width">0.4</sld:CssParameter>
              <sld:CssParameter name="stroke-opacity">0.3</sld:CssParameter>
            </sld:Stroke>
          </sld:PolygonSymbolizer>
        </sld:Rule>
	  <Rule>
      <Name>CPOB_CNMBR</Name>
	  <sld:MaxScaleDenominator>1500000</sld:MaxScaleDenominator>
	  <TextSymbolizer>
	    <Label>
              <ogc:PropertyName>CPOB_CNMBR</ogc:PropertyName>
            </Label>
            <Font>
	      <CssParameter name="font-family">arial</CssParameter>
	      <CssParameter name="font-size">9</CssParameter>
	      <CssParameter name="font-style">normal</CssParameter>
	      <CssParameter name="font-weight">normal</CssParameter>
            </Font>
			 <sld:Fill>
              <sld:CssParameter name="fill">#185be2</sld:CssParameter>
              <sld:CssParameter name="fill-opacity">1.0</sld:CssParameter>
            </sld:Fill>
	   <LabelPlacement>
           <PointPlacement>
             <AnchorPoint>
               <AnchorPointX>1</AnchorPointX>
               <AnchorPointY>1</AnchorPointY>
             </AnchorPoint>
			 <Rotation>0</Rotation>
             <Displacement>
               <DisplacementX>1</DisplacementX>
               <DisplacementY>7</DisplacementY>
             </Displacement>
           </PointPlacement>
         </LabelPlacement>
		</TextSymbolizer>
	</Rule> 
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>
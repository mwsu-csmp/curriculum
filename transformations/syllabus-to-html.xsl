<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
  xmlns="https://csmp.missouriwestern.edu"
  xmlns:csmp="https://csmp.missouriwestern.edu"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
  <body>
    <h1><xsl:value-of select="csmp:course/csmp:title"/></h1>

    <h2>Objectives</h2>
    <ul>
      <xsl:for-each select="csmp:course/csmp:objectives/csmp:objective">
        <li><xsl:value-of select="current()"/></li>
      </xsl:for-each>
    </ul>

  </body>
</html>
</xsl:template>

</xsl:stylesheet>

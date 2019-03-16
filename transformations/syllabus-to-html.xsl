<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
  xmlns="https://csmp.missouriwestern.edu"
  xmlns:csmp="https://csmp.missouriwestern.edu"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
  <body>
    <h1>Missouri Western State University</h1>
    <h1>College of Liberal Arts and Sciences</h1>
    <h2>Department of Computer Science, Math, and Physics</h2>
    <div class="field"><span class="label">Course Number</span>: <xsl:value-of select="csmp:course/csmp:subject"/> <xsl:value-of select="csmp:course/csmp:number"/></div>
    <div class="field"><span class="label">Course Name</span>: <xsl:value-of select="csmp:course/csmp:title"/></div>

    <div class="field"><span class="label">Prerequisites</span>: 
      <xsl:for-each select="csmp:course/csmp:prerequisites/csmp:prerequisite">
        <xsl:value-of select="current()"/> 
          <xsl:if test="@corequisite='true'"><xsl:text> (concurrent OK)</xsl:text></xsl:if>
          <xsl:if test="position() != last()"><xsl:text>,</xsl:text></xsl:if>&#160;
      </xsl:for-each>
    </div>
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

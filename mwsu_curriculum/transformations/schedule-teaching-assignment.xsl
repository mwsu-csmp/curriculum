<?xml version="1.0"?>
<?xml-stylesheet href="XsltVersion" type="text/xml"?>

<xsl:stylesheet version="1.0"
  xmlns="https://csmp.missouriwestern.edu"
  xmlns:csmp="https://csmp.missouriwestern.edu"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes" />
<!-- variables needed to bring add in multiple sections per course-->
<xsl:variable name="end" select="number(14)" />
<xsl:variable name="increment" select="number(1)"/>

<xsl:template match="/">
<html>
  <body>
    <h1>Missouri Western State University</h1>
    <h1>College of Liberal Arts and Sciences</h1>
    <h2>Schedule Course List</h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th style="text-align:left">Instructor</th>
        <th style="text-align:left">Course</th>
        <th style="text-align:left">Section</th>
        <th style="text-align:left">Time</th>
        <th style="text-align:left">Days</th>
        <th style="text-align:left">Bldg/Rm</th>
        <th style="text-align:left">Max</th>
      </tr>

      <tr>
        <xsl:variable name="start" select="number(1)"/>
        <xsl:for-each select="//csmp:course/csmp:section/csmp:instructor[not(.=preceding::*)]">
        <xsl:call-template name="subject">
        <xsl:with-param name="counter" select="$start"/>
        </xsl:call-template>
        <xsl:for-each select="//csmp:course">
        <xsl:call-template name="subjectInfo">
        <xsl:with-param name="counter" select="$start"/>
        </xsl:call-template>
        </xsl:for-each>
        </xsl:for-each>
      </tr>

    </table>
  </body>
</html>
</xsl:template>

<!-- first loop contains the information for each class. Which include section, time, days, building/room, max seats, and instrustor G# -->
<xsl:template name="subjectInfo">
  <xsl:param name = "counter"/>
  <xsl:if test=" @type = 'instructor'">
  <tr>
  <td></td>
  <td><xsl:value-of select="csmp:subject"/><xsl:value-of select="csmp:number"/></td>
  <td><xsl:value-of select="csmp:section/csmp:sectionNumber"/></td>
  <td><xsl:value-of select="csmp:section/csmp:StartTime"/> - <xsl:value-of select="csmp:section/csmp:EndTime"/></td>
  <td>
    <xsl:for-each select="csmp:section/csmp:day">
      <xsl:value-of select="."/>
    </xsl:for-each>
  </td>
  <td><xsl:value-of select="csmp:section/csmp:buildingRoom"/></td>
  <td><xsl:value-of select="csmp:section/csmp:max"/></td>
  <td><xsl:value-of select="csmp:section/csmp:instructor"/></td>
  </tr>
  <xsl:call-template name="subjectInfo">
  </xsl:call-template>
  </xsl:if>
</xsl:template>

<!-- This loop just brings in the subject and number for the course. ex) ACT102 -->
<xsl:template name="subject">
  <xsl:param name = "counter"/>
  <xsl:if test="$counter &lt;= $end">
  <tr><td><xsl:value-of select="."/></td></tr>
  <xsl:call-template name="subject">
  </xsl:call-template>
  </xsl:if>
</xsl:template>

</xsl:stylesheet>

#!/usr/bin/env python

"""
To test the program:
% TestWCDB2.py >& TestWCDB2.out
"""

# -------
# imports
# -------

import StringIO
import unittest

from WCDB2 import *


# -----------
# TestWCDB2
# -----------

c = login()

class Node(object):
  
  ''' Test class to represent an ambiguous object with attribute "text". '''

  def __init__(self, text=None):
    self.text = text


class TestWCDB2(unittest.TestCase) :
  # -------
  # Login
  # -------
  
  def test_Login_1(self):
    conn = login()
    self.assert_(conn)

  #--------
  #Get_text
  #--------

  def test_get_text(self):
    node = Node()
    self.assert_(get_text(node) == '""')

  def test_get_text_2(self):
    node = Node()
    node.text = "some text"
    self.assert_(get_text(node) == '"some text"')

  def test_get_text_3(self):
    node = Node("more text")
    self.assert_(get_text(node) == '"more text"')

  #--------
  #Escape_quote
  #--------

  def test_escape_quote_1(self):
    text = 'test this " text'
    self.assert_(escape_quote(text) == 'test this \\" text')

  def test_escape_quote_2(self):
    text = 'try with two "" text'
    self.assert_(escape_quote(text) == 'try with two \\"\\" text')

  def test_escape_quote_3(self):
    text = 'test "" this " text'
    self.assert_(escape_quote(text) == 'test \\"\\" this \\" text')

  #--------
  #Import
  #--------

  def test_import_1(self):
    root = ET.fromstring("<WorldCrises></WorldCrises>")
    wcdb2_import(root)
    self.assert_(query(c, 'SELECT * from Person') == ())
    self.assert_(query(c, 'SELECT * from Crisis') == ())
    self.assert_(query(c, 'SELECT * from Organization') == ())
    self.assert_(query(c, 'SELECT * from Location') == ())
    self.assert_(query(c, 'SELECT * from HumanImpact') == ())
    self.assert_(query(c, 'SELECT * from WaysToHelp') == ())

  def test_import_2(self):
    root = ET.fromstring("""
<WorldCrises>
  <Person personIdent="BHObama">
    <Name>
      <FirstName>Barack</FirstName>
      <MiddleName>Hussein</MiddleName>
      <LastName>Obama</LastName>
      <Suffix>II</Suffix>
    </Name>
    <Kind personKindIdent="PR"/>
  </Person>

  <Person personIdent="OBLaden">
    <Name>
      <FirstName>Osama</FirstName>
      <MiddleName>bin Mohammed bin Awad</MiddleName>
      <LastName>bin Laden</LastName>
    </Name>
    <Kind personKindIdent="LD"/>
  </Person>

  <Person personIdent="GWBush">
    <Name>
      <FirstName>George</FirstName>
      <MiddleName>Walker</MiddleName>
      <LastName>Bush</LastName>
    </Name>
    <Kind personKindIdent="PR"/>
  </Person>

  <Person personIdent="JVStalin">
    <Name>
      <FirstName>Joseph</FirstName>
      <MiddleName>Vissarionovic</MiddleName>
      <LastName>Stalin</LastName>
    </Name>
    <Kind personKindIdent="LD"/>
</Person>

<Person personIdent="BHGates">
  <Name>
    <FirstName>Bill</FirstName>
    <MiddleName>Henry</MiddleName>
    <LastName>Gates</LastName>
    <Suffix>III</Suffix>
  </Name>
  <Kind personKindIdent="PH"/>
</Person>

  <Person personIdent="MHThatcher">
    <Name>
      <FirstName>Margaret</FirstName>
      <MiddleName>Hilda</MiddleName>
      <LastName>Thatcher</LastName>
    </Name>
    <Kind personKindIdent="PM"/>
  </Person>

  <Person personIdent="KPapoulias">
    <Name>
      <FirstName>Karolos</FirstName>
      <LastName>Papoulias</LastName>
    </Name>
    <Kind personKindIdent="PR"/>
  </Person>

  <Person personIdent="JGZuma">
    <Name>
      <FirstName>Jacob</FirstName>
      <MiddleName>Gedleyihlekisa</MiddleName>
      <LastName>Zuma</LastName>
    </Name>
    <Kind personKindIdent="PR"/>
</Person>

<Person personIdent="AMRAl-Zawahiri">
  <Name>
    <FirstName>Ayman</FirstName>
    <MiddleName>Mohhammed Rabie</MiddleName>
    <LastName>al-Zawahiri</LastName>
  </Name>
  <Kind personKindIdent="LD"/>
</Person>

  <Person personIdent="RNMcEntire">
    <Name>
      <FirstName>Reba</FirstName>
      <MiddleName>Nell</MiddleName>
      <LastName>McEntire</LastName>
    </Name>
    <Kind personKindIdent="SNG"/>
  </Person>
</WorldCrises>
""")
    wcdb2_import(root)
    t = query(c, 'SELECT * from Person')
    self.assert_(t == (('BHObama', 'Barack', 'Hussein', 'Obama', 'II', 'PR'), \
('OBLaden', 'Osama', 'bin Mohammed bin Awad', 'bin Laden', None, 'LD'), \
('GWBush', 'George', 'Walker', 'Bush', None, 'PR'), \
('JVStalin', 'Joseph', 'Vissarionovic', 'Stalin', None, 'LD'), \
('BHGates', 'Bill', 'Henry', 'Gates', 'III', 'PH'), \
('MHThatcher', 'Margaret', 'Hilda', 'Thatcher', None, 'PM'), \
('KPapoulias', 'Karolos', None, 'Papoulias', None, 'PR'), \
('JGZuma', 'Jacob', 'Gedleyihlekisa', 'Zuma', None, 'PR'), \
('AMRAl-Zawahiri', 'Ayman', 'Mohhammed Rabie', 'al-Zawahiri', None, 'LD'), \
('RNMcEntire', 'Reba', 'Nell', 'McEntire', None, 'SNG')))

  def test_import_3(self):
    root = ET.fromstring("""
    <WorldCrises>
      <Crisis crisisIdent="Shirley_WAR_2013">
        <Name>2013 Great Attack of Shirley</Name>
        <Kind crisisKindIdent="WAR"/>
        <Location>
          <Locality>Houston</Locality>
          <Country>USA</Country>
        </Location>
        <StartDateTime>
          <Date>2013-04-01</Date>
        </StartDateTime>
        <HumanImpact>
          <Type>Death</Type>
          <Number>1</Number>
        </HumanImpact>
        <EconomicImpact>72000000000000000000000000000</EconomicImpact>
        <ResourceNeeded>Cash</ResourceNeeded>
        <WaysToHelp></WaysToHelp>
        <ExternalResources></ExternalResources>
      </Crisis>

      <Organization organizationIdent="HSO">
        <Name>Help Shirley Organization</Name>
        <Kind organizationKindIdent="HO"/>
        <Location>
          <Locality>Houston</Locality>
          <Country>USA</Country>
        </Location>
      <History>
        Shirley got pissed off from working so hard.
      </History>
      <ContactInfo>
        <Telephone>1 800 733 2767</Telephone>
        <Fax>202 303 4498</Fax>
        <Email>shirley@example.com</Email>
        <PostalAddress>
          <StreetAddress>2025 E Street</StreetAddress>
          <Locality>Washinton</Locality>
          <Region>DC</Region>
          <PostalCode>20006</PostalCode>
          <Country>United States</Country>
        </PostalAddress>
      </ContactInfo>
      <ExternalResources>
        <ImageURL>http://carladavisshow.com/wp-content/uploads/2012/11/red-cross1.jpg</ImageURL>
      </ExternalResources>
    </Organization>

    <Person personIdent="SLi">
      <Name>
        <FirstName>Shirley</FirstName>
        <LastName>Li</LastName>
      </Name>
      <Kind personKindIdent="PR"/>
      <Location>
        <Locality>Houston</Locality>
        <Region>Texas</Region>
        <Country>United States</Country>
      </Location>
      <ExternalResources>
        <ImageURL>https://sphotos-a.xx.fbcdn.net/hphotos-snc6/249035_10150943750989530_1854017333_n.jpg</ImageURL>
      </ExternalResources>
    </Person>

    <CrisisKind crisisKindIdent="WAR">
      <Name>War</Name>
      <Description>An organized and often prolonged conflict that is carried out by states and/or non-state actors.</Description>
    </CrisisKind>

    <OrganizationKind organizationKindIdent="HO">
      <Name>Humanitarian Organization</Name>
      <Description>Organization that provides humanitarian aid</Description>
    </OrganizationKind>

    <PersonKind personKindIdent="PR">
      <Name>President</Name>
      <Description>Leader or the government of some countries</Description>
    </PersonKind>

    </WorldCrises>
    """)
    wcdb2_import(root)
    self.assert_(query(c, 'SELECT * from Person') == (('SLi', \
'Shirley', None, 'Li', None, 'PR'),))
    self.assert_(query(c, 'SELECT * from WaysToHelp') == (('1', \
'Shirley_WAR_2013', ''),))

  #--------
  #Export
  #--------
  
  def test_export_1(self):
    wcdb2_import(ET.fromstring("<WorldCrises/>"))
    outroot = wcdb2_export(c)
    outstring = ET.tostring(outroot, pretty_print=True)
    self.assert_(outstring == '<WorldCrises/>\n')

  def test_export_2(self):
    wcdb2_import(ET.fromstring("<WorldCrises></WorldCrises>"))
    outroot = wcdb2_export(c)
    outstring = ET.tostring(outroot, pretty_print=True)
    self.assert_(outstring == '<WorldCrises/>\n')

  def test_export_3(self):
    wcdb2_import(ET.fromstring("""
    <WorldCrises>
      <Crisis crisisIdent="Shirley_WAR_2013">
        <Name>2013 Great Attack of Shirley</Name>
        <Kind crisisKindIdent="WAR"/>
        <Location>
          <Locality>Houston</Locality>
          <Country>USA</Country>
        </Location>
        <StartDateTime>
          <Date>2013-12-01</Date>
        </StartDateTime>
        <HumanImpact>
          <Type>Death</Type>
          <Number>999999999999999999999999</Number> <!-- limited to int-->
        </HumanImpact>
        <EconomicImpact></EconomicImpact>
        <ResourceNeeded></ResourceNeeded>
        <WaysToHelp></WaysToHelp>
        <ExternalResources></ExternalResources>
      </Crisis>
    <CrisisKind crisisKindIdent="WAR">
      <Name>War</Name>
      <Description>An organized and often "prolonged conflict is carried out by states and/or non-state actors.</Description>
    </CrisisKind>

    <OrganizationKind organizationKindIdent="HO">
      <Name>Humanitarian Organization</Name>
      <Description>Organization that provides humanitarian aid</Description>
    </OrganizationKind>

    <PersonKind personKindIdent="PR">
      <Name>President</Name>
      <Description>Leader or the government of some countries</Description>
    </PersonKind>

    </WorldCrises>
    """))
    outroot = wcdb2_export(c)
    outstring = ET.tostring(outroot)
    self.assert_(outstring == '<WorldCrises><Crisis crisisIdent="Shirley_WAR_2013"><Name>2013 Great Attack of Shirley</Name><Kind crisisKindIdent="WAR"/><Location><Locality>Houston</Locality><Country>USA</Country></Location><StartDateTime><Date>2013-12-01</Date></StartDateTime><HumanImpact><Type>Death</Type><Number>2147483647</Number></HumanImpact><EconomicImpact></EconomicImpact><ResourceNeeded></ResourceNeeded><WaysToHelp></WaysToHelp><ExternalResource/><RelatedPersons/><RelatedOrganizations/></Crisis><CrisisKind crisisKindIdent="WAR"><Name>War</Name><Description>An organized and often "prolonged conflict is carried out by states and/or non-state actors.</Description></CrisisKind><OrganizationKind organizationKindIdent="HO"><Name>Humanitarian Organization</Name><Description>Organization that provides humanitarian aid</Description></OrganizationKind><PersonKind personKindIdent="PR"><Name>President</Name><Description>Leader or the government of some countries</Description></PersonKind></WorldCrises>')


# main
# ----

print "TestWCDB2.py"
unittest.main()
print "done."

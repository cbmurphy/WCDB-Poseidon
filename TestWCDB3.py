#!/usr/bin/env python

"""
To test the program:
% TestWCDB3.py >& TestWCDB3.out
"""

# -------
# imports
# -------

import StringIO
import unittest

from WCDB3 import *

# -----------
# TestWCDB3
# -----------

c = login()
def drop_all():
  drop_tmp = [
  """ DROP TABLE IF EXISTS Crisis;""",
  """ DROP TABLE IF EXISTS Organization;""",
  """ DROP TABLE IF EXISTS Person;""",
  """ DROP TABLE IF EXISTS Location;""",
  """ DROP TABLE IF EXISTS HumanImpact;""",
  """ DROP TABLE IF EXISTS ResourceNeeded;""",
  """ DROP TABLE IF EXISTS WaysToHelp;""",
  """ DROP TABLE IF EXISTS ExternalResource;""",
  """ DROP TABLE IF EXISTS CrisisOrganization;""",
  """ DROP TABLE IF EXISTS OrganizationPerson;""",
  """ DROP TABLE IF EXISTS PersonCrisis;""",
  """ DROP TABLE IF EXISTS CrisisKind;""",
  """ DROP TABLE IF EXISTS OrganizationKind;""",
  """ DROP TABLE IF EXISTS PersonKind;""",
  ]
  for q in drop_tmp:
    t = query(c, q)

class Node(object):
  
  ''' Test class to represent an ambiguous object with attribute "text". '''

  def __init__(self, text=None):
    self.text = text


class TestWCDB3(unittest.TestCase) :
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

  # -------
  # read
  # -------
  
  def test_wcdb3_read_1(self):
    r = StringIO.StringIO("<a />")
    root = wcdb3_read(r)
    self.assert_(root.tag == "a")


  def test_wcdb3_read_2(self):
    r = StringIO.StringIO("<a> <b></b> </a>")
    root = wcdb3_read(r)
    self.assert_(root.tag == "a")
    self.assert_(root[0].tag == "b")

  def test_wcdb3_read_3(self):
    r = StringIO.StringIO("<a>hello world</a>")
    root = wcdb3_read(r)
    self.assert_(root.tag == "a")
    self.assert_(root.text == "hello world")

  # -------
  # write
  # -------

  def test_wcdb3_write_1(self):
    w = StringIO.StringIO()
    a = ET.Element('a')
    wcdb3_write(a, w)
    self.assert_(w.getvalue() == "<a/>\n")

  def test_wcdb3_write_2(self):
    w = StringIO.StringIO()
    a = ET.Element('a')
    b = ET.SubElement(a, 'b')
    wcdb3_write(a, w)
    self.assert_(w.getvalue() == "<a>\n  <b/>\n</a>\n")

  def test_wcdb3_write_3(self):
    w = StringIO.StringIO()
    a = ET.Element('a')
    a.text = "hello world"
    wcdb3_write(a, w)
    self.assert_(w.getvalue() == "<a>hello world</a>\n")

  #--------
  #Solve
  #--------
  
  def test_wcdb3_sove_1(self):
    r = StringIO.StringIO("""
    <WoldCrises>
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
          <ImageURL>https://.jpg</ImageURL>
        </ExternalResources>
      </Person>
    </WoldCrises>
    """)
    w = StringIO.StringIO()
    wcdb3_solve([r], w, True) 
    self.assert_(w.getvalue() =="""<WorldCrises>
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
      <ImageURL>https://.jpg</ImageURL>
    </ExternalResources>
    <RelatedCrises/>
    <RelatedOrganizations/>
  </Person>
</WorldCrises>
""")

  def test_wcdb3_sove_2(self):
    r1 = StringIO.StringIO("""
    <WoldCrises>
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
          <ImageURL>https://.jpg</ImageURL>
        </ExternalResources>
      </Person>
    </WoldCrises>
    """)
    r2 = StringIO.StringIO("""
    <WoldCrises>
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
          <ImageURL>https://1.jpg</ImageURL>
        </ExternalResources>
      </Person>
    </WoldCrises>
    """)
    w = StringIO.StringIO()
    wcdb3_solve([r1, r2], w, True) 
    self.assert_(w.getvalue() =="""<WorldCrises>
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
      <ImageURL>https://.jpg</ImageURL>
      <ImageURL>https://1.jpg</ImageURL>
    </ExternalResources>
    <RelatedCrises/>
    <RelatedOrganizations/>
  </Person>
</WorldCrises>
""")

  def test_wcdb3_solve_3(self):
    r1 = StringIO.StringIO("""<WorldCrises>
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

    r2 = StringIO.StringIO("""<WorldCrises>
      <Crisis crisisIdent="Shirley_WAR_2013">
        <Name>2013 Great Attack by Shirley</Name>
        <Kind crisisKindIdent="WAR"/>
        <Location>
          <Locality>Austin</Locality>
          <Country>USA</Country>
        </Location>
        <StartDateTime>
          <Date>2014-04-01</Date>
        </StartDateTime>
        <HumanImpact>
          <Type>Death</Type>
          <Number>0</Number>
        </HumanImpact>
        <EconomicImpact>0</EconomicImpact>
        <ResourceNeeded>Food</ResourceNeeded>
        <WaysToHelp></WaysToHelp>
        <ExternalResources></ExternalResources>
      </Crisis>

      <Organization organizationIdent="HSO">
        <Name>Help Shirley?</Name>
        <Kind organizationKindIdent="HO"/>
        <Location>
          <Locality>Austin</Locality>
          <Country>USA</Country>
        </Location>
      <History>
        Shirley got pissed off from working so hard?
      </History>
      <ContactInfo>
        <Telephone>1 800 733 2767</Telephone>
        <Fax>202 303 4498</Fax>
        <Email>shirley@gmail.com</Email>
        <PostalAddress>
          <StreetAddress>2025 W Street</StreetAddress>
          <Locality>Washinton</Locality>
          <Region>DC</Region>
          <PostalCode>2013</PostalCode>
          <Country>United States</Country>
        </PostalAddress>
      </ContactInfo>
      <ExternalResources>
        <ImageURL>http://.jpg</ImageURL>
      </ExternalResources>
    </Organization>

    <Person personIdent="SLi">
      <Name>
        <FirstName>Xueli</FirstName>
        <LastName>Li</LastName>
      </Name>
      <Kind personKindIdent="PR"/>
      <Location>
        <Locality>Austin</Locality>
        <Region>Texas</Region>
        <Country>United States</Country>
      </Location>
      <ExternalResources>
        <ImageURL>1.jpg</ImageURL>
      </ExternalResources>
    </Person>

    <CrisisKind crisisKindIdent="WAR">
      <Name>War</Name>
      <Description>An organized</Description>
    </CrisisKind>

    <OrganizationKind organizationKindIdent="HO">
      <Name>Humanitarian Organization</Name>
      <Description>that provides humanitarian aid</Description>
    </OrganizationKind>

    <PersonKind personKindIdent="PR">
      <Name>President</Name>
      <Description>Leader</Description>
    </PersonKind>

    </WorldCrises>
    """)

    w = StringIO.StringIO()
    wcdb3_solve([r1, r2], w, True) 
    self.assert_(w.getvalue() =="""<WorldCrises>
  <Crisis crisisIdent="Shirley_WAR_2013">
    <Name>2013 Great Attack by Shirley</Name>
    <Kind crisisKindIdent="WAR"/>
    <Location>
      <Locality>Houston</Locality>
      <Country>USA</Country>
    </Location>
    <Location>
      <Locality>Austin</Locality>
      <Country>USA</Country>
    </Location>
    <StartDateTime>
      <Date>2014-04-01</Date>
    </StartDateTime>
    <HumanImpact>
      <Type>Death</Type>
      <Number>1</Number>
    </HumanImpact>
    <EconomicImpact>0</EconomicImpact>
    <ResourceNeeded>Cash</ResourceNeeded>
    <ResourceNeeded>Food</ResourceNeeded>
    <WaysToHelp></WaysToHelp>
    <ExternalResources/>
    <RelatedPersons/>
    <RelatedOrganizations/>
  </Crisis>
  <Organization organizationIdent="HSO">
    <Name>Help Shirley?</Name>
    <Kind organizationKindIdent="HO"/>
    <Location>
      <Locality>Houston</Locality>
      <Country>USA</Country>
    </Location>
    <Location>
      <Locality>Austin</Locality>
      <Country>USA</Country>
    </Location>
    <History>
        Shirley got pissed off from working so hard?
      </History>
    <ContactInfo>
      <Telephone>1 800 733 2767</Telephone>
      <Fax>202 303 4498</Fax>
      <Email>shirley@gmail.com</Email>
      <PostalAddress>
        <StreetAddress>2025 W Street</StreetAddress>
        <Locality>Washinton</Locality>
        <Region>DC</Region>
        <PostalCode>2013</PostalCode>
        <Country>United States</Country>
      </PostalAddress>
    </ContactInfo>
    <ExternalResources>
      <ImageURL>http://carladavisshow.com/wp-content/uploads/2012/11/red-cross1.jpg</ImageURL>
      <ImageURL>http://.jpg</ImageURL>
    </ExternalResources>
    <RelatedCrises/>
    <RelatedPersons/>
  </Organization>
  <Person personIdent="SLi">
    <Name>
      <FirstName>Xueli</FirstName>
      <LastName>Li</LastName>
    </Name>
    <Kind personKindIdent="PR"/>
    <Location>
      <Locality>Houston</Locality>
      <Region>Texas</Region>
      <Country>United States</Country>
    </Location>
    <Location>
      <Locality>Austin</Locality>
      <Region>Texas</Region>
      <Country>United States</Country>
    </Location>
    <ExternalResources>
      <ImageURL>https://sphotos-a.xx.fbcdn.net/hphotos-snc6/249035_10150943750989530_1854017333_n.jpg</ImageURL>
      <ImageURL>1.jpg</ImageURL>
    </ExternalResources>
    <RelatedCrises/>
    <RelatedOrganizations/>
  </Person>
  <CrisisKind crisisKindIdent="WAR">
    <Name>War</Name>
    <Description>An organized</Description>
  </CrisisKind>
  <OrganizationKind organizationKindIdent="HO">
    <Name>Humanitarian Organization</Name>
    <Description>that provides humanitarian aid</Description>
  </OrganizationKind>
  <PersonKind personKindIdent="PR">
    <Name>President</Name>
    <Description>Leader</Description>
  </PersonKind>
</WorldCrises>
""")
    
  #--------
  #Import
  #--------

  def test_import_1(self):
    drop_all()
    root = ET.fromstring("<WorldCrises></WorldCrises>")
    wcdb3_import(root, True, True)
    self.assert_(query(c, 'SELECT * from Person') == ())
    self.assert_(query(c, 'SELECT * from Crisis') == ())
    self.assert_(query(c, 'SELECT * from Organization') == ())
    self.assert_(query(c, 'SELECT * from Location') == ())
    self.assert_(query(c, 'SELECT * from HumanImpact') == ())
    self.assert_(query(c, 'SELECT * from WaysToHelp') == ())
    drop_all()

  def test_import_2(self):
    drop_all()
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
    wcdb3_import(root, True, True)
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
    drop_all()

  def test_import_3(self):
    drop_all()
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
    wcdb3_import(root, True, True)
    self.assert_(query(c, 'SELECT * from Person') == (('SLi', \
      'Shirley', None, 'Li', None, 'PR'),))
    self.assert_(query(c, 'SELECT * from WaysToHelp') == (('1', \
      'Shirley_WAR_2013', ''),))
    drop_all()


  def test_import_4(self):
    drop_all()
    root = ET.fromstring("""
    <WoldCrises>
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
          <ImageURL>https://.png</ImageURL>
        </ExternalResources>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root,True, True)

    root = ET.fromstring("""
    <WoldCrises>
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
          <ImageURL>https://.jpg</ImageURL>
        </ExternalResources>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root, False, True)
    self.assert_(query(c, 'SELECT link  from ExternalResource') == \
        (('https://.png',),('https://.jpg',)))
    drop_all()


  def test_import_5(self):
    drop_all()
    root = ET.fromstring(
    """
    <WoldCrises>
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
          <ImageURL>https://.jpg</ImageURL>
        </ExternalResources>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root, False, True)
    root = ET.fromstring(
    """
    <WoldCrises>
      <Person personIdent="JMENG">
        <Name>
          <FirstName>Jianyong</FirstName>
          <LastName>Meng</LastName>
        </Name>
        <Kind personKindIdent="LD"/>
        <Location>
          <Locality>Austin</Locality>
          <Region>Texas</Region>
          <Country>United States</Country>
        </Location>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root, False, True)

    self.assert_(query(c, 'SELECT * from Person') == \
        (('SLi', 'Shirley', None, 'Li', None, 'PR'), \
        ('JMENG', 'Jianyong', None, 'Meng', None, 'LD')))
    drop_all()

  def test_import_6(self):
    drop_all()
    root = ET.fromstring(
    """
    <WoldCrises>
      <Person personIdent="JMENG">
        <Name>
          <FirstName>Jianyong</FirstName>
          <LastName>Meng</LastName>
        </Name>
        <Kind personKindIdent="LD"/>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root, True, True)

    root = ET.fromstring(
    """
    <WoldCrises>
      <Person personIdent="JMENG">
        <Name>
          <FirstName>Jianyong</FirstName>
          <MiddleName>Morris</MiddleName>
          <LastName>Meng</LastName>
        </Name>
        <Kind personKindIdent="LD"/>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root, False, True)
    self.assert_(query(c, 'SELECT * from Person') == \
        (('JMENG', 'Jianyong', None, 'Meng', None, 'LD'),))
    drop_all()
  
  def test_import_7(self):
    drop_all()
    root = ET.fromstring(
    """
    <WoldCrises>
      <Person personIdent="JMENG">
        <Name>
          <FirstName>Jianyong</FirstName>
          <LastName>Meng</LastName>
        </Name>
        <Kind personKindIdent="LD"/>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root)
    root = ET.fromstring(
    """
    <WoldCrises>
      <Person personIdent="JMENG">
        <Name>
          <FirstName>Daniel</FirstName>
          <LastName>Meng</LastName>
        </Name>
        <Kind personKindIdent="LD"/>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root)
    self.assert_(query(c, 'SELECT * from Person') == \
        (('JMENG', 'Daniel', None, 'Meng', None, 'LD'),))
    drop_all()
    
  def test_import_8(self):
    drop_all()
    root = ET.fromstring(
    """
    <WoldCrises>
      <Person personIdent="JMENG">
        <Name>
          <FirstName>Jianyong</FirstName>
          <LastName>Meng</LastName>
        </Name>
        <Kind personKindIdent="LD"/>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root)

    root = ET.fromstring(
    """
    <WoldCrises>
      <Person personIdent="JMENG">
        <Name>
          <FirstName>Daniel</FirstName>
          <LastName>Meng</LastName>
        </Name>
        <Kind personKindIdent="LD"/>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root, False, True)
    self.assert_(query(c, 'SELECT * from Person') == \
        (('JMENG', 'Jianyong', None, 'Meng', None, 'LD'),))
    drop_all()
    
  def test_import_9(self):
    drop_all()
    root = ET.fromstring("""
    <WoldCrises>
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
          <ImageURL>https://.png</ImageURL>
        </ExternalResources>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root)

    root = ET.fromstring("""
    <WoldCrises>
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
          <ImageURL>https://.jpg</ImageURL>
        </ExternalResources>
      </Person>
    </WoldCrises>
    """)
    wcdb3_import(root)
    self.assert_(query(c, 'SELECT link  from ExternalResource') == \
        (('https://.png',),('https://.jpg',)))
    drop_all()

  def test_import_10(self):
    drop_all()
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
        <EconomicImpact>0</EconomicImpact>
        <ResourceNeeded>Cash</ResourceNeeded>
        <WaysToHelp></WaysToHelp>
        <ExternalResources></ExternalResources>
      </Crisis>
    </WorldCrises>
    """)
    wcdb3_import(root)
    self.assert_(query(c, 'SELECT economic_impact from Crisis') == (('0',),)) 
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
        <EconomicImpact>5</EconomicImpact>
        <ResourceNeeded>Cash</ResourceNeeded>
        <WaysToHelp></WaysToHelp>
        <ExternalResources></ExternalResources>
      </Crisis>
    </WorldCrises>
    """)
    wcdb3_import(root)
    
    self.assert_(query(c, 'SELECT economic_impact from Crisis') == (('5',),)) 
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
        <EconomicImpact>3</EconomicImpact>
        <ResourceNeeded>Cash</ResourceNeeded>
        <WaysToHelp></WaysToHelp>
        <ExternalResources></ExternalResources>
      </Crisis>
    </WorldCrises>
    """)
    wcdb3_import(root)
    
    self.assert_(query(c, 'SELECT economic_impact from Crisis') == (('3',),)) 
    drop_all()

  #--------
  #Export
  #--------
  
  def test_export_1(self):
    drop_all()
    wcdb3_import(ET.fromstring("<WorldCrises/>"))
    outroot = wcdb3_export(c)
    outstring = ET.tostring(outroot, pretty_print=True)
    self.assert_(outstring == '<WorldCrises/>\n')
    drop_all()

  def test_export_2(self):
    drop_all()
    wcdb3_import(ET.fromstring("<WorldCrises></WorldCrises>"))
    outroot = wcdb3_export(c)
    outstring = ET.tostring(outroot, pretty_print=True)
    self.assert_(outstring == '<WorldCrises/>\n')
    drop_all()

  def test_export_3(self):
    drop_all()
    wcdb3_import(ET.fromstring("""
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
    outroot = wcdb3_export(c)
    outstring = ET.tostring(outroot, pretty_print = True)
    self.assert_(outstring == """<WorldCrises>
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
      <Number>2147483647</Number>
    </HumanImpact>
    <EconomicImpact>0</EconomicImpact>
    <ResourceNeeded></ResourceNeeded>
    <WaysToHelp></WaysToHelp>
    <ExternalResources/>
    <RelatedPersons/>
    <RelatedOrganizations/>
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
""")

    drop_all()

# main
# ----

print "TestWCDB3.py"
unittest.main()
print "done."

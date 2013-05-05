#!/usr/bin/env python

import sys
#import xml.etree.ElementTree as ET
from WCDB2_import import *
from lxml import etree as ET
from Login import *
from Query import *

# ------------
# wcdb2_export 
# ------------

def wcdb2_export(c):
  """
  export a DB to an ElementTree
  c is mysql connection object 
  returns outroot, an Element Tree
  """

  outroot = ET.Element('WorldCrises')
  # export Crisis
  t = query(c, "select * from Crisis")
  for row in t:
    Crisis = ET.SubElement(outroot, 'Crisis')
    Crisis.set('crisisIdent', row[0])
    Name = ET.SubElement(Crisis, 'Name')
    Name.text = row[1]
    Kind = ET.SubElement(Crisis, 'Kind')
    Kind.set('crisisKindIdent', row[2])

    qstring = """select Locality, Region, Country
                 from Location
                 where entity_id = '%s' and entity_type = '%s'
              """ %(row[0], 'C')
    tt = query(c, qstring)
    
    for rrow in tt:
      Location = ET.SubElement(Crisis, 'Location')
      if rrow[0] is not None:
        Locality = ET.SubElement(Location, 'Locality')
        Locality.text = rrow[0]
      if rrow[1] is not None:
        Region = ET.SubElement(Location, 'Region')
        Region.text = rrow[1]
      if rrow[2] is not None:
        Country = ET.SubElement(Location, 'Country')
        Country.text = rrow[2]

    StartDateTime = ET.SubElement(Crisis, 'StartDateTime')
    StartDate = ET.SubElement(StartDateTime, 'Date')
    StartDate.text = row[3]
    if row[4] is not None:
      StartTime = ET.SubElement(StartDateTime, 'Time')
      StartTime.text = row[4]
    if row[5] is not None:
      EndDateTime = ET.SubElement(Crisis, 'EndDateTime')
      EndDate = ET.SubElement(EndDateTime, 'Date')
      EndDate.text = row[5]
      if row[6] is not None:
        EndTime = ET.SubElement(EndDateTime, 'Time')
        EndTime.text = row[6]

    qstring = """select Type, Number 
                 from HumanImpact 
                 where crisis_id = '%s'
              """ %(row[0])
    tt = query(c, qstring)
    
    for rrow in tt:
      HumanImpact = ET.SubElement(Crisis,'HumanImpact') 
      Type = ET.SubElement(HumanImpact, 'Type')
      Type.text = rrow[0]
      Number = ET.SubElement(HumanImpact, 'Number')
      Number.text = rrow[1]

    EconomicImpact = ET.SubElement(Crisis, 'EconomicImpact')
    EconomicImpact.text = row[7]

    qstring = """select description 
                 from ResourceNeeded 
                 where crisis_id = '%s'
              """ %(row[0])
    tt = query(c, qstring)
    
    for rrow in tt:
      ResourceNeeded = ET.SubElement(Crisis,'ResourceNeeded') 
      ResourceNeeded.text = rrow[0]

    qstring = """select description 
                 from WaysToHelp 
                 where crisis_id = '%s'
              """ %(row[0])
    tt = query(c, qstring)
    
    for rrow in tt:
      WaysToHelp = ET.SubElement(Crisis,'WaysToHelp') 
      WaysToHelp.text = rrow[0]
    
    # ExternalResource

    ExternalResource = ET.SubElement(Crisis,'ExternalResource') 
    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('C', row[0], 'IMAGE')
    tt = query(c, qstring)
    
    for rrow in tt:
      ImageURL = ET.SubElement(ExternalResource,'ImageURL') 
      ImageURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('C', row[0], 'VIDEO')
    tt = query(c, qstring)
   
    for rrow in tt:
      VideoURL = ET.SubElement(ExternalResource,'VideoURL') 
      VideoURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('C', row[0], 'MAP')
    tt = query(c, qstring)
    
    for rrow in tt:
      MapURL = ET.SubElement(ExternalResource,'MapURL') 
      MapURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('C', row[0], 'SOCIAL_NETWORK')
    tt = query(c, qstring)
    
    for rrow in tt:
      SocialNetworkURL = ET.SubElement(ExternalResource,'SocialNetworkURL') 
      SocialNetworkURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('C', row[0], 'CITATION')
    tt = query(c, qstring)
    
    for rrow in tt:
      Citation = ET.SubElement(ExternalResource,'Citation') 
      Citation.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('C', row[0], 'EXTERNAL_LINK')
    tt = query(c, qstring)
    
    for rrow in tt:
      ExternalLinkURL = ET.SubElement(ExternalResource,'ExternalLinkURL') 
      ExternalLinkURL.text = rrow[0]
      
    qstring = """select id_person 
                 from PersonCrisis 
                 where id_crisis = '%s' 
              """ %(row[0] )
    tt = query(c, qstring)
    if tt is not None:
      RelatedPersons = ET.SubElement(Crisis, 'RelatedPersons')
    for rrow in tt:
      RelatedPerson = ET.SubElement(RelatedPersons, 'RelatedPerson')
      RelatedPerson.set('personIdent', rrow[0])

    qstring = """select id_organization 
                 from CrisisOrganization 
                 where id_crisis = '%s' 
              """ %(row[0] )
    tt = query(c, qstring)
    if tt is not None:
      RelatedOrganizations = ET.SubElement(Crisis, 'RelatedOrganizations')
    for rrow in tt:
      RelatedOrganization = ET.SubElement(RelatedOrganizations, 'RelatedOrganization')
      RelatedOrganization.set('organizationIdent', rrow[0])
        
  # export Organization 
  t = query(c, "select * from Organization")
  for row in t:
    Organization = ET.SubElement(outroot, 'Organization')
    Organization.set('organizationIdent', row[0])
    Name = ET.SubElement(Organization, 'Name')
    Name.text = row[1]
    Kind = ET.SubElement(Organization, 'Kind')
    Kind.set('organizationKindIdent', row[2])

    qstring = """select Locality, Region, Country
                 from Location
                 where entity_id = '%s' and entity_type = '%s'
              """ %(row[0], 'O')
    tt = query(c, qstring)
    
    for rrow in tt:
      Location = ET.SubElement(Organization, 'Location')
      if rrow[0] is not None:
        Locality = ET.SubElement(Location, 'Locality')
        Locality.text = rrow[0]
      if rrow[1] is not None:
        Region = ET.SubElement(Location, 'Region')
        Region.text = rrow[1]
      if rrow[2] is not None:
        Country = ET.SubElement(Location, 'Country')
        Country.text = rrow[2]

    History = ET.SubElement(Organization, 'History')
    History.text = row[3]
    ContactInfo = ET.SubElement(Organization, 'ContactInfo')
    Telephone = ET.SubElement(ContactInfo, 'Telephone')
    Telephone.text = row[4]
    Fax = ET.SubElement(ContactInfo, 'Fax')
    Fax.text = row[5]
    Email = ET.SubElement(ContactInfo, 'Email')
    Email.text = row[6]
    PostalAddress = ET.SubElement(ContactInfo, 'PostalAddress')
    StreetAddress = ET.SubElement(PostalAddress, 'StreetAddress')
    StreetAddress.text = row[7]
    Locality = ET.SubElement(PostalAddress, 'Locality')
    Locality.text = row[8]
    Region = ET.SubElement(PostalAddress, 'Region')
    Region.text = row[9]
    PostalCode = ET.SubElement(PostalAddress, 'PostalCode')
    PostalCode.text = row[10]
    Country = ET.SubElement(PostalAddress, 'Country')
    Country.text = row[11]

    # ExternalResources
    ExternalResource = ET.SubElement(Organization,'ExternalResource') 
    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('O', row[0], 'IMAGE')
    tt = query(c, qstring)
    
    for rrow in tt:
      ImageURL = ET.SubElement(ExternalResource,'ImageURL') 
      ImageURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('O', row[0], 'VIDEO')
    tt = query(c, qstring)
    
    for rrow in tt:
      VideoURL = ET.SubElement(ExternalResource,'VideoURL') 
      VideoURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('O', row[0], 'MAP')
    tt = query(c, qstring)
    
    for rrow in tt:
      MapURL = ET.SubElement(ExternalResource,'MapURL') 
      MapURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('O', row[0], 'SOCIAL_NETWORK')
    tt = query(c, qstring)
    
    for rrow in tt:
      SocialNetworkURL = ET.SubElement(ExternalResource,'SocialNetworkURL') 
      SocialNetworkURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('O', row[0], 'CITATION')
    tt = query(c, qstring)
    
    for rrow in tt:
      Citation = ET.SubElement(ExternalResource,'Citation') 
      Citation.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('O', row[0], 'EXTERNAL_LINK')
    tt = query(c, qstring)
    
    for rrow in tt:
      ExternalLinkURL = ET.SubElement(ExternalResource,'ExternalLinkURL') 
      ExternalLinkURL.text = rrow[0]
    
    # RelatedCrises
    qstring = """select id_crisis 
                 from CrisisOrganization 
                 where id_organization = '%s' 
              """ %(row[0] )
    tt = query(c, qstring)
    if tt is not None:
      RelatedCrises = ET.SubElement(Organization, 'RelatedCrises')
    for rrow in tt:
      RelatedCrisis = ET.SubElement(RelatedCrises, 'RelatedCrisis')
      RelatedCrisis.set('crisisIdent', rrow[0])

    #RelatedPersons
    qstring = """select id_person 
                 from OrganizationPerson 
                 where id_organization = '%s' 
              """ %(row[0] )
    tt = query(c, qstring)
    if tt is not None:
      RelatedPersons = ET.SubElement(Organization, 'RelatedPersons')
    for rrow in tt:
      RelatedPerson = ET.SubElement(RelatedPersons, 'RelatedPerson')
      RelatedPerson.set('personIdent', rrow[0])

  # export Person 
  t = query(c, "select * from Person")
  for row in t:
    Person = ET.SubElement(outroot, 'Person')
    Person.set('personIdent', row[0])
    Name = ET.SubElement(Person, 'Name')
    FirstName = ET.SubElement(Name, 'FirstName')
    FirstName.text = row[1]
    if row[2] is not None:
      MiddleName = ET.SubElement(Name, 'MiddleName')
      MiddleName.text = row[2]
    LastName = ET.SubElement(Name, 'LastName')
    LastName.text = row[3]
    if row[4] is not None:
      Suffix = ET.SubElement(Name, 'Suffix')
      Suffix.text = row[4]
    Kind = ET.SubElement(Person, 'Kind')
    Kind.set('personKindIdent', row[5])

    # Location
    qstring = """select Locality, Region, Country
                 from Location
                 where entity_id = '%s' and entity_type = '%s'
              """ %(row[0], 'P')
    tt = query(c, qstring)
    
    for rrow in tt:
      Location = ET.SubElement(Person, 'Location')
      if rrow[0] is not None:
        Locality = ET.SubElement(Location, 'Locality')
        Locality.text = rrow[0]
      if rrow[1] is not None:
        Region = ET.SubElement(Location, 'Region')
        Region.text = rrow[1]
      if rrow[2] is not None:
        Country = ET.SubElement(Location, 'Country')
        Country.text = rrow[2]

    # ExternalResources
    ExternalResource = ET.SubElement(Person,'ExternalResource') 
    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('P', row[0], 'IMAGE')
    tt = query(c, qstring)
    
    for rrow in tt:
      ImageURL = ET.SubElement(ExternalResource,'ImageURL') 
      ImageURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('P', row[0], 'VIDEO')
    tt = query(c, qstring)
    
    for rrow in tt:
      VideoURL = ET.SubElement(ExternalResource,'VideoURL') 
      VideoURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('P', row[0], 'MAP')
    tt = query(c, qstring)
    
    for rrow in tt:
      MapURL = ET.SubElement(ExternalResource,'MapURL') 
      MapURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('P', row[0], 'SOCIAL_NETWORK')
    tt = query(c, qstring)
    
    for rrow in tt:
      SocialNetworkURL = ET.SubElement(ExternalResource,'SocialNetworkURL') 
      SocialNetworkURL.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('P', row[0], 'CITATION')
    tt = query(c, qstring)
    
    for rrow in tt:
      Citation = ET.SubElement(ExternalResource,'Citation') 
      Citation.text = rrow[0]

    qstring = """select link 
                 from ExternalResource 
                 where entity_type = '%s' 
                       and entity_id = '%s' 
                       and type = '%s'
              """ %('P', row[0], 'EXTERNAL_LINK')
    tt = query(c, qstring)
    
    for rrow in tt:
      ExternalLinkURL = ET.SubElement(ExternalResource,'ExternalLinkURL') 
      ExternalLinkURL.text = rrow[0]
    
    # RelatedCrises
    qstring = """select id_crisis 
                 from PersonCrisis 
                 where id_person = '%s' 
              """ %(row[0] )
    tt = query(c, qstring)
    if tt is not None:
      RelatedCrises = ET.SubElement(Person, 'RelatedCrises')
    for rrow in tt:
      RelatedCrisis = ET.SubElement(RelatedCrises, 'RelatedCrisis')
      RelatedCrisis.set('crisisIdent', rrow[0])

    # RelatedOrganizations
    qstring = """select id_organization 
                 from OrganizationPerson 
                 where id_person = '%s' 
              """ %(row[0] )
    tt = query(c, qstring)
    if tt is not None:
      RelatedOrganizations = ET.SubElement(Person, 'RelatedOrganizations')
    for rrow in tt:
      RelatedOrganization = ET.SubElement(RelatedOrganizations, 'RelatedOrganization')
      RelatedOrganization.set('organizationIdent', rrow[0])

  # export CrisisKind
  t = query(c, "select * from CrisisKind")
  for row in t:
    CrisisKind = ET.SubElement(outroot, 'CrisisKind')
    CrisisKind.set('crisisKindIdent', row[0])
    Name = ET.SubElement(CrisisKind, 'Name')
    Name.text = row[1]
    Description = ET.SubElement(CrisisKind, 'Description')
    Description.text = row[2]
  # export OrganizationKind
  t = query(c, "select * from OrganizationKind")
  for row in t:
    OrganizationKind = ET.SubElement(outroot, 'OrganizationKind')
    OrganizationKind.set('organizationKindIdent', row[0])
    Name = ET.SubElement(OrganizationKind, 'Name')
    Name.text = row[1]
    Description = ET.SubElement(OrganizationKind, 'Description')
    Description.text = row[2]
  # export PersonKind
  t = query(c, "select * from PersonKind")
  for row in t:
    PersonKind = ET.SubElement(outroot, 'PersonKind')
    PersonKind.set('personKindIdent', row[0])
    Name = ET.SubElement(PersonKind, 'Name')
    Name.text = row[1]
    Description = ET.SubElement(PersonKind, 'Description')
    Description.text = row[2]

  return outroot



# ----
# main
# ----

if __name__ == "__main__":
  c = login()
  tree = ET.parse('WCDB1.xml')
  root = tree.getroot()
  
  # import
  wcdb2_import(root)
  outroot = wcdb2_export(c);
  print ET.tostring(outroot, pretty_print = True)

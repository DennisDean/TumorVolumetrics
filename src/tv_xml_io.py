<?xml version="1.0" encoding="utf-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           elementFormDefault="qualified"
           attributeFormDefault="unqualified">

  <!-- Root -->
  <xs:element name="TumorVolumeDataset">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Contributors" type="ContributorsType"/>
        <xs:element name="Experiments" type="ExperimentsType"/>
      </xs:sequence>
      <xs:attribute name="version" type="xs:string" use="optional"/>
    </xs:complexType>
  </xs:element>

  <!-- Contributors -->
  <xs:complexType name="ContributorsType">
    <xs:sequence>
      <xs:element name="Contributor" type="ContributorType" maxOccurs="unbounded"/>
    </xs:sequence>
  </xs:complexType>

  <xs:complexType name="ContributorType">
    <xs:sequence>
      <xs:element name="Name" type="xs:string"/>
      <xs:element name="DiseaseTypes" minOccurs="0">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="DiseaseType" type="DiseaseTypeType" maxOccurs="unbounded"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
      <xs:element name="Experiments" minOccurs="0">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="ExperimentRef" type="xs:IDREF" maxOccurs="unbounded"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
    </xs:sequence>
    <xs:attribute name="id" type="xs:ID" use="required"/>
  </xs:complexType>

  <xs:complexType name="DiseaseTypeType">
    <xs:simpleContent>
      <xs:extension base="xs:string">
        <xs:attribute name="id" type="xs:ID" use="required"/>
      </xs:extension>
    </xs:simpleContent>
  </xs:complexType>

  <!-- Experiments -->
  <xs:complexType name="ExperimentsType">
    <xs:sequence>
      <xs:element name="Experiment" type="ExperimentType" maxOccurs="unbounded"/>
    </xs:sequence>
  </xs:complexType>

  <xs:complexType name="ExperimentType">
    <xs:sequence>
      <xs:element name="ContributorRef" type="xs:IDREF"/>
      <xs:element name="DiseaseTypeRef" type="xs:IDREF" minOccurs="0"/>
      <xs:element name="Description" type="xs:string" minOccurs="0"/>
      <xs:element name="Studies">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="Study" type="StudyType" maxOccurs="unbounded"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
    </xs:sequence>
    <xs:attribute name="id" type="xs:ID" use="required"/>
  </xs:complexType>

  <xs:complexType name="StudyType">
    <xs:sequence>
      <xs:element name="Name" type="xs:string" minOccurs="0"/>
      <xs:element name="Arms">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="Arm" type="ArmType" maxOccurs="unbounded"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
    </xs:sequence>
    <xs:attribute name="id" type="xs:ID" use="required"/>
  </xs:complexType>

  <xs:complexType name="ArmType">
    <xs:sequence>
      <xs:element name="Name" type="xs:string" minOccurs="0"/>
      <xs:element name="MatchedControls" type="xs:boolean" minOccurs="0"/>
      <xs:element name="TumorVolumeCurves">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="TumorVolumeCurve" type="TumorVolumeCurveType" maxOccurs="unbounded"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
    </xs:sequence>
    <xs:attribute name="id" type="xs:ID" use="required"/>
  </xs:complexType>

  <xs:complexType name="TumorVolumeCurveType">
    <xs:sequence>
      <xs:element name="SubjectID" type="xs:string" minOccurs="0"/>
      <xs:element name="TumorID" type="xs:string" minOccurs="0"/>
      <xs:element name="Demographics" minOccurs="0">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="BodyWeight" minOccurs="0">
              <xs:complexType>
                <xs:simpleContent>
                  <xs:extension base="xs:decimal">
                    <xs:attribute name="unit" type="xs:string" use="optional" default="g"/>
                  </xs:extension>
                </xs:simpleContent>
              </xs:complexType>
            </xs:element>
            <xs:element name="Age" type="xs:decimal" minOccurs="0"/>
            <xs:element name="Sex" type="xs:string" minOccurs="0"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>

      <xs:element name="Measurements">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="Measurement" type="MeasurementType" maxOccurs="unbounded"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>

      <xs:element name="MatchedControlRefs" minOccurs="0">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="CurveRef" type="xs:IDREF" maxOccurs="unbounded"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>

    </xs:sequence>
    <xs:attribute name="id" type="xs:ID" use="required"/>
  </xs:complexType>

  <xs:complexType name="MeasurementType">
    <xs:sequence>
      <xs:element name="Time">
        <xs:complexType>
          <xs:simpleContent>
            <xs:extension base="xs:decimal">
              <xs:attribute name="unit" type="xs:string" use="optional" default="day"/>
            </xs:extension>
          </xs:simpleContent>
        </xs:complexType>
      </xs:element>
      <xs:element name="Volume">
        <xs:complexType>
          <xs:simpleContent>
            <xs:extension base="xs:decimal">
              <xs:attribute name="unit" type="xs:string" use="optional" default="mm3"/>
            </xs:extension>
          </xs:simpleContent>
        </xs:complexType>
      </xs:element>
    </xs:sequence>
  </xs:complexType>

</xs:schema>

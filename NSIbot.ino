#include <SharpIR.h>
#include <Wire.h>
#include <math.h>
#include "Weights.h"
/* Mode 0 par défaut pour MD25*/

#define CMD (byte)0x00     // Values of 0 eing sent using write have to be cast as a byte to stop them being misinterperted as NULL \
  // This is a but with arduino 1
#define MD25ADDRESS 0x58   // Address of the MD25
#define SPEED1 (byte)0x00  // Byte to send speed to first motor
#define SPEED2 0x01        // Byte to send speed to second motor
#define ENCODERONE 0x02    // Byte to read motor encoder 1
#define ENCODERTWO 0x06    // Byte to read motor encoder 2
#define RESETENCODERS 0x20

//Télémètres en entrées analogiques (CAN 10 bits)
#define IRPin1 A6
#define IRPin2 A2
#define IRPin3 A4  //
#define modelSharp 1080

#define DETECT_DIST 40   // Distance maxi 15 cm
#define VITESSE_MIN 78   // Commande vitesse minimum MD25
#define VITESSE_MAX 178  // Commande vitesse maximum MD25

/* Instanciations Objets "Télémétres"*/
SharpIR Telm_AVG = SharpIR(IRPin1, modelSharp);
SharpIR Telm_AV = SharpIR(IRPin2, modelSharp);
SharpIR Telm_AVD = SharpIR(IRPin3, modelSharp);

int i, j, p, q, r;
float Accum;

/* Définition réseau de neurones*/
const int PatternCount = 8;  //paramètres pour le réseau Neuronal 3 couches 3/4/2

float Hidden[HiddenNodes];
float Output[OutputNodes];  //Sortie du réseau neuronal

void InputToOutput(float In1, float In2, float In3)  //Fonction de conversion d'entrée en sortie du réseau neuronal
{
  float RealInput[] = { 0, 0, 0 };
  RealInput[0] = In1;
  RealInput[1] = In2;
  RealInput[2] = In3;

  /******************************************************************
    Compute hidden layer activations
  ******************************************************************/

  for (i = 0; i < HiddenNodes; i++) {
    Accum = 0.0;                        // Init Accum
    // Multiplie la matrice d'entrée par la matrice de poids cachés et réalise la sigmoïd
    for (j = 0; j < InputNodes; j++) {  //
      Accum += RealInput[j] * HiddenWeights[j][i];
    }
    Hidden[i] = 1.0 / (1.0 + exp(-Accum));
  }

  /******************************************************************
    Compute output layer activations and calculate errors
  ******************************************************************/

  for (i = 0; i < OutputNodes; i++) {
    Accum = 0.0;
    //Multiplie la matrice précédente par la matrice de poids de sortie et réalise la sigmoïd
    for (j = 0; j < HiddenNodes; j++) {
      Accum += Hidden[j] * OutputWeights[j][i];
    }
    Output[i] = 1.0 / (1.0 + exp(-Accum));
  }
}
/* Vérification sur terminal série*/
//  Serial.print ("  Output ");
//  for ( i = 0 ; i < OutputNodes ; i++ )
//      {
//    Serial.print (Output[i], 5);
//    Serial.print(" ");
//    }
//  Serial.println(" ");}



/* Gestion Moteurs EMG30 via MD25*/

/* Contrôle vistesse Moteur ARDroit: MotD */

void Cmd_MotD(int Vit1) {
  Wire.beginTransmission(MD25ADDRESS);  // Drive motor 1 at speed value vit1
  Wire.write(SPEED1);
  Wire.write(Vit1);
  Wire.endTransmission();
}

/* Contrôle vistesse Moteur ARGauche: MotG */
void Cmd_MotG(int Vit2) {
  Wire.beginTransmission(MD25ADDRESS);  // Drive motor 2 at speed value vit2
  Wire.write(SPEED2);
  Wire.write(Vit2);
  Wire.endTransmission();
}

/* Gestion télémètres */
/*Distance en cm entre le capteur et les obstacles*/
int distance_cmAV;
int distance_cmAVD;
int distance_cmAVG;

float coeffMotorG;  // Coefficient commande moteurs G et D
float coeffMotorD;

unsigned int dGauche;
unsigned int dAvant;
unsigned int dDroite;

float fGauche;
float fAvant;
float fDroite;


void setup() {
  Serial.begin(9600);
  Wire.begin();
  delay(100);
}

void loop() {
  /*récupère les distances en cm renvoyées par les télémètres*/
  distance_cmAV = Telm_AV.distance();
  distance_cmAVG = Telm_AVG.distance();
  distance_cmAVD = Telm_AVD.distance();

  /* Limitation des distances mesurables */
  if (distance_cmAVG < 10) distance_cmAVG = 10;
  if (distance_cmAVG > DETECT_DIST) distance_cmAVG = DETECT_DIST;
  if (distance_cmAVD < 10) distance_cmAVD = 10;
  if (distance_cmAVD > DETECT_DIST) distance_cmAVD = DETECT_DIST;
  if (distance_cmAV < 10) distance_cmAV = 10;
  if (distance_cmAV > DETECT_DIST) distance_cmAV = DETECT_DIST;

  dGauche = map(distance_cmAVG, 10, DETECT_DIST, 0, 255);  //Transforme les valeurs de distance en valeurs comprises entre 0 et 255
  dAvant = map(distance_cmAV, 10, DETECT_DIST, 0, 255);
  dDroite = map(distance_cmAVD, 10, DETECT_DIST, 0, 255);

  fGauche = dGauche / 256.0;  //Divise les valeurs par 256 pour qu'elles soient comprisent
  fAvant = dAvant / 256.0;    // entre 0.0(proche de 10cm) et 1.0 (>= à DETECT_DISTcm)
  fDroite = dDroite / 256.0;

  InputToOutput(fGauche, fAvant, fDroite);  //Transforme les valeurs des capteurs en valeur de controle des moteurs

  coeffMotorG = (Output[0]);  //Récupère les valeurs de sortie
  coeffMotorD = (Output[1]);

  Cmd_MotD(VITESSE_MIN + coeffMotorD * 100);
  Cmd_MotG(VITESSE_MAX - coeffMotorG * 100);
}

import java.io.*;
import java.net.*;
import java.util.Scanner;
import java.util.Random;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;


public class client {
    public static void main(String[] args) {
        String serverAddress = args[0]; // argument for hostname
        int serverPort = Integer.parseInt(args[1]); // argument for port
        Random rand = new Random();
        int requestId = rand.nextInt(100); // request id
        boolean cont = true;
        Scanner reader = new Scanner(System.in);
        while (cont) {
            try (Socket socket = new Socket(serverAddress, serverPort)) {
                int[] inputs = getInputs(reader);
                int[] message = new int[2];
                // Calculates the total size of packet and size of opName based on opcode choice
                if (inputs[0] == 3) { // the or opcode
                    message[0] = 15;
                    message[1] = 6;
                } else {
                    message[0] = 17;
                    message[1] = 8;
                }

                String opName = getOpName(inputs[0]);
                ByteBuffer buffer = ByteBuffer.allocate(message[0]); // uses total length for creating a packet

                buffer.putShort((short) message[0]); // tml
                buffer.put((byte) inputs[0]); // opCode
                buffer.putShort((short) inputs[1]); // operand 1
                buffer.putShort((short) inputs[2]); // operand 2
                buffer.put((byte) requestId);
                buffer.put((byte) message[1]); // length of operation name
                buffer.putShort((short) 65279); // byte order "FE FF" Network Byte Order

                byte[] opNameBytes = opName.getBytes(StandardCharsets.UTF_8);
                for (byte b : opNameBytes) {
                    buffer.put((byte) 0x00); // ensures the corrrect position of bytes for operation name
                    buffer.put(b);
                }

                byte[] byteMessage = buffer.array();
                System.out.println("Sending this data: ");
                for (byte b : byteMessage) {
                    System.out.printf("%02X ", b);
                }

                OutputStream outputStream = socket.getOutputStream(); // establish input output streams
                InputStream inputStream = socket.getInputStream();

                long startTime = System.currentTimeMillis();

                outputStream.write(byteMessage); // send message

                ByteArrayOutputStream buffer2 = new ByteArrayOutputStream();
                int bytesRead;
                byte[] data = new byte[1024]; // Read in chunks of 1024 bytes

                while ((bytesRead = inputStream.read(data, 0, data.length)) != -1) {
                    buffer2.write(data, 0, bytesRead);
                }
                
                byte[] responseBytes = buffer2.toByteArray();
                // reads all recieved bytes

                System.out.println("\nResponse Recieved:");
                for (byte b : responseBytes) {
                    System.out.printf("%02X ", b);
                }

                ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(responseBytes); // gets input and
                                                                                                     // makes it
                                                                                                     // readable data
                DataInputStream responseStream = new DataInputStream(byteArrayInputStream); // creates a parsable data
                                                                                            // stream

                int ttl = responseStream.readUnsignedShort();
                long endTime = System.currentTimeMillis();
                int reqId = responseStream.readUnsignedByte();
                int result = responseStream.readInt();
                int errorCode = responseStream.readByte();

                if (ttl != 8) {
                    System.out.println("Total Length in Responce Wrong!");
                }

                System.out.println("\nRequest ID: " + reqId);
                System.out.println("Result: " + result);
                if (errorCode == 0) {
                    System.out.println("Error Code: Ok");
                } else {
                    System.out.println("Error Code: Bad Request");
                }

                long totalTime = endTime - startTime;
                System.out.println("Responce Time: " + totalTime + " ms");

                while (true) {
                    try {
                        System.out.println("Would You Like To Send Another Message(1 for Yes, 2 for No): ");
                        int n = reader.nextInt();
                        if (n == 1) {
                            break;
                        }
                        if (n == 2) {
                            cont = false;
                            break;
                        } else {
                            throw new Exception();
                        }
                    } catch (Exception e) {
                        System.out.print("\nInvalid Input");
                        reader.nextLine();
                    }
                }
            } catch (Exception e) {
                System.err.println(e);
                break;
            }
        }
        reader.close();
    }

    public static String getOpName(int opCode) {
        switch (opCode) {
            case 0:
                return "div";
            case 1:
                return "mul";
            case 2:
                return "and";
            case 3:
                return "or";
            case 4:
                return "add";
            case 5:
                return "sub";
        }
        return "";
    }

    public static int[] getInputs(Scanner reader) {
        int[] inputs = new int[3];
        while (true) {
            try {
                System.out.print("Please Choose The First Number In The Operation:\n");
                int n = reader.nextInt();
                if (n < -32767 || n > 32767) { // max signed integer for 2 bytes
                    throw new Exception();
                } else {
                    inputs[1] = n;
                    break;
                }
            } catch (Exception e) {
                System.out.print("Invalid Input");
                reader.nextLine();
            }
        }
        while (true) {
            try {
                System.out.print(
                        "Please Select A Number Based On The Given Table:\nOperation: / | * | & | | | + | - |\n   OpCode: 0 | 1 | 2 | 3 | 4 | 5 |\n");
                int n = reader.nextInt();
                if (n < 0 || n > 5) {
                    throw new Exception();
                } else {
                    inputs[0] = n;
                    break;
                }
            } catch (Exception e) {
                System.out.print("Invalid Input");
                reader.nextLine();
            }
        }
        while (true) {
            try {
                System.out.print("Please Choose The Second Number In The Operation:\n");
                int n = reader.nextInt();
                if (n < -32767 || n > 32767) { // max signed integer for 2 bytes
                    throw new Exception();
                } else {
                    inputs[2] = n;
                    break;
                }
            } catch (Exception e) {
                System.out.print("Invalid Input");
                reader.nextLine();
            }
        }
        return inputs;
    }
}

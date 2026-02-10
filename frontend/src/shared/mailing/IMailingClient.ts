export interface IMailingClient {
  addSubject(subject: string): IMailingClient
  addTextBody(text: string): IMailingClient
  addHtmlBody(html: string): IMailingClient
  sendEmail(reciever_address: string): Promise<boolean>
}

from mco_agent import Agent, action, dispatch, register_actions


@register_actions
class Parrot(Agent):

    @action
    def echo(self):
        """ Responds with the given input

        :param request:
        return:
        """
        self.reply.data['message'] = self.request.data['message']

    @action
    def invalid(self):
        self.reply.fail(1, "Invalid command")


if __name__ == '__main__':
    dispatch(Parrot)
